/*
 *  Open Fodder
 *  ---------------
 *
 *  Copyright (C) 2008-2026 Open Fodder
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License along
 *  with this program; if not, write to the Free Software Foundation, Inc.,
 *  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 */

#include "Utils/SurfaceDraw.hpp"
#include "Utils/SurfaceLayers.hpp"
#include "Utils/PausePresentation.hpp"
#include "Utils/MissionPresentation.hpp"
#include "Utils/MissionLayers.hpp"
#include <cstdlib>
#include <mutex>
#include <atomic>
#include <cstdio>

const size_t		 g_MaxColors = 0xFF;

class cPalette {
public:
	uint8 mRed;
	uint8 mGreen;
	uint8 mBlue;

	cPalette() { mRed = 0; mGreen = 0; mBlue = 0; }

	uint8 getPos( size_t i ) { if (i == 0) return mRed; if (i == 1) return mGreen; if (i == 2) return mBlue; return 0; }
	void setPos( size_t i, uint8 pval ) {
		if( i == 0 )
			mRed = pval;
		if( i == 1 )
			mGreen = pval;
		if( i == 2 )
			mBlue = pval;
	}
};


// Full indexed copy state. Save buffer and fade-adjusting flag are deliberately
// absent: classic copyFrom does not copy them.
struct IndexedSurfaceState {
    openfodder::IndexedLayer layer;
    std::array<cPalette, 255> current, next;
    std::array<uint32, 255> effective;
};

class cSurface {
protected:
    struct MissionAuditRecording {
        uint64_t interval = openfodder::NextPresentationSerial();
        std::mutex mutex;
        openfodder::MissionLayerSequence scene;
        std::shared_ptr<const openfodder::SoldierPose> pose;
        bool replacePose = false;
    };
    std::shared_ptr<MissionAuditRecording> mMissionAudit;
    openfodder::PresentationDestinationId mPresentationDestination =
        std::make_shared<const openfodder::PresentationDestination>();
    bool PresentationDestinationMatches(const openfodder::PresentationDestinationId& identity,
        size_t width, size_t height, size_t stride, size_t count) const;
    bool            mIsLoadedImage;
	cPalette		mPalette[ g_MaxColors ];
	cPalette		mPaletteNew[ g_MaxColors ];

	uint32			mPaletteSDL[ g_MaxColors ]{};

	uint8*			mSurfaceBuffer;								// Loaded Image (uses palette indexs)
	uint8*			mSurfaceBufferSaved;
	size_t			mSurfaceBufferSize;

	SDL_Surface*	mSDLSurface;
	SDL_Texture*	mTexture;

	size_t			mWidth, mHeight;
	bool			mPaletteAdjusting;


	void			clearSDLSurface(uint32 pColor = 0);						// Clear the surface

	void			paletteSDLColorSet( size_t id, cPalette *pPalette  );	// Set a color in the palette
	

public:
    // Optional retained publication always keeps the classic producer oracle.
    static bool MissionPublicationEnabled() {
        const char* enabled = std::getenv("OPENFODDER_PRESENT_MISSION_LAYERS");
        return enabled && std::string(enabled) == "1";
    }
    static int MissionPresentationRepeats(bool unitTesting) {
        if (!unitTesting || !MissionPublicationEnabled()) return 1;
        const char* value = std::getenv("OPENFODDER_TEST_MISSION_PRESENTATIONS");
        if (!value) return 1;
        const std::string option(value);
        if (option != "0" && option != "1" && option != "5")
            throw std::invalid_argument("mission presentation test count must be 0, 1 or 5");
        const int repeats = option[0] - '0';
        static std::atomic<bool> announced{false};
        if (!announced.exchange(true))
            std::fprintf(stderr, "MISSION_LAYER_SCHEDULE: %d presentations per mission call\n", repeats);
        return repeats;
    }
    bool MissionAuditActive() const { return bool(std::atomic_load(&mMissionAudit)); }
    void RecordMissionLayer(openfodder::MissionLayer layer) {
        const auto recording = std::atomic_load(&mMissionAudit);
        if (!recording) return;
        layer.destination = mPresentationDestination;
        std::lock_guard<std::mutex> lock(recording->mutex);
        recording->scene.layers.push_back(std::move(layer));
    }
    void RecordMissionPixels(const openfodder::IndexedProducerDraw& pixels,
                             openfodder::MissionLayerRole role = openfodder::MissionLayerRole::Sprite) {
        if (!MissionAuditActive()) return;
        openfodder::MissionLayer layer; layer.role = role;
        layer.pixels = pixels; RecordMissionLayer(std::move(layer));
    }
    void RecordMissionSoldier(const openfodder::PreparedSpriteDraw& prepared) {
        const auto recording = std::atomic_load(&mMissionAudit);
        if (!recording) return;
        openfodder::MissionLayer layer;
        layer.destination = mPresentationDestination;
        layer.role = openfodder::MissionLayerRole::Sprite;
        layer.operation = openfodder::MissionLayerOperation::Soldier;
        layer.soldier = prepared;
        layer.soldier.soldier.interval = recording->interval;
        // No borrowed draw pointer is needed by the semantic consumer.
        layer.soldier.draw.source = nullptr;
        std::lock_guard<std::mutex> lock(recording->mutex);
        if (recording->replacePose) {
            if (recording->pose && recording->pose->origin.soldier.scene != prepared.soldier.scene)
                recording->pose.reset();
            if (!recording->pose)
                recording->pose = openfodder::CaptureOriginalSoldierPose(layer.soldier);
            layer.pose = recording->pose;
        }
        recording->scene.layers.push_back(std::move(layer));
    }
    void RecordMissionTerrain(const openfodder::TerrainDraw& terrain) {
        if (!MissionAuditActive()) return;
        openfodder::MissionLayer layer; layer.role = openfodder::MissionLayerRole::Terrain;
        layer.operation = openfodder::MissionLayerOperation::Terrain;
        layer.terrain = terrain; RecordMissionLayer(std::move(layer));
    }
    void RecordMissionSidebar(const openfodder::SidebarDraw& sidebar) {
        if (!MissionAuditActive()) return;
        openfodder::MissionLayer layer; layer.role = openfodder::MissionLayerRole::Sidebar;
        layer.operation = openfodder::MissionLayerOperation::Sidebar;
        layer.sidebar = sidebar; RecordMissionLayer(std::move(layer));
    }
    void RecordMissionSurface(openfodder::MissionLayerOperation operation, uint8 color = 0) {
        if (!MissionAuditActive()) return;
        openfodder::MissionLayer layer; layer.operation = operation; layer.clearIndex = color;
        RecordMissionLayer(std::move(layer));
    }
    void BeginMissionAudit(cSurface* other, bool eligible) {
        const auto previous = std::atomic_load(&mMissionAudit);
        // Reset at every producer iteration, including zero presentations and pause.
        std::atomic_store(&mMissionAudit, std::shared_ptr<MissionAuditRecording>{});
        if (other && other != this)
            std::atomic_store(&other->mMissionAudit, std::shared_ptr<MissionAuditRecording>{});
        const char* enabled = std::getenv("OPENFODDER_AUDIT_MISSION_LAYERS");
        if (!eligible || isLoadedImage() ||
            (!MissionPublicationEnabled() && (!enabled || std::string(enabled) != "1"))) return;
        const auto recording = std::make_shared<MissionAuditRecording>();
        const char* poseOption = std::getenv("OPENFODDER_REPLACE_SOLDIER_POSE");
        recording->replacePose = poseOption && std::string(poseOption) == "1";
        if (recording->replacePose && previous) {
            std::lock_guard<std::mutex> lock(previous->mutex);
            recording->pose = previous->pose;
        }
        auto attach = [&](cSurface* surface) {
            if (!surface || surface->isLoadedImage()) return;
            recording->scene.destinations.push_back({surface->CapturePresentation(),
                openfodder::CaptureLayer(surface->mSurfaceBufferSaved, surface->mSurfaceBufferSize,
                    surface->mWidth, surface->mHeight, surface->mWidth)});
        };
        attach(this);
        if (other != this) attach(other);
        std::atomic_store(&mMissionAudit, recording);
        if (other && other != this && !other->isLoadedImage())
            std::atomic_store(&other->mMissionAudit, recording);
    }
    openfodder::MissionLayerSequence VerifyMissionAudit(const cSurface* other,
        openfodder::PresentationTarget* publication = nullptr) const {
        const auto recording = std::atomic_load(&mMissionAudit);
        if (!recording) return {};
        openfodder::MissionLayerSequence scene;
        {
            std::lock_guard<std::mutex> lock(recording->mutex);
            scene = recording->scene;
        }
        std::vector<const cSurface*> actual;
        for (auto& source : scene.destinations) {
            const cSurface* surface = source.initial.destination == mPresentationDestination ? this : other;
            if (!surface || source.initial.destination != surface->mPresentationDestination)
                throw std::runtime_error("mission audit: destination replaced during recording");
            const auto current = surface->CaptureDraw();
            if (!current.indices || current.width != source.initial.indexed.width ||
                current.height != source.initial.indexed.height)
                throw std::runtime_error("mission audit: incompatible indexed destination");
            // Palette is sampled at the real conversion point, after late fades.
            source.initial.indexed.colors = current.colors;
            actual.push_back(surface);
        }
        const auto composed = openfodder::ComposeMissionLayers(scene);
        for (size_t i = 0; i < actual.size(); ++i) {
            const auto* surface = actual[i];
            if (*composed.surfaces[i].indexed.indices != *surface->CaptureDraw().indices ||
                !std::equal(composed.saved[i].pixels->begin(), composed.saved[i].pixels->end(),
                            surface->mSurfaceBufferSaved))
                throw std::runtime_error("mission audit: unrecorded or reordered indexed write");
            const auto expected = openfodder::RasterizePresentationSurface(surface->CapturePresentation());
            auto replay = openfodder::RasterizePresentationSurface(composed.surfaces[i]);
            if (expected.destination != replay.destination || expected.width != replay.width ||
                expected.height != replay.height || expected.stride != replay.stride || expected.pixels != replay.pixels)
                throw std::runtime_error("mission audit: composed frame differs from classic frame");
            // Publish precisely the pixels just checked, not a new classic capture.
            if (publication && surface == this) *publication = std::move(replay);
        }
        for (const auto& layer : scene.layers) {
            if (layer.operation != openfodder::MissionLayerOperation::Soldier) continue;
            static std::atomic<uint64_t> soldierScene{0};
            const auto identity = layer.soldier.soldier.scene;
            if (soldierScene.exchange(identity) != identity)
                std::fprintf(stderr, "SOLDIER_SEMANTIC: verified original resource in mission composition scene=%llu\n",
                    static_cast<unsigned long long>(identity));
            break;
        }
        if (recording->replacePose) {
            const auto substituted = openfodder::ComposeMissionLayers(scene, true);
            // This pilot uses original artwork: both paths MUST remain identical.
            // A defect is never disguised as a missing-asset fallback.
            for (size_t i = 0; i < actual.size(); ++i) {
                if (*substituted.surfaces[i].indexed.indices != *composed.surfaces[i].indexed.indices ||
                    *substituted.saved[i].pixels != *composed.saved[i].pixels)
                    throw std::runtime_error("soldier pose: replacement differs from original");
                auto replay = openfodder::RasterizePresentationSurface(substituted.surfaces[i]);
                if (replay.pixels != openfodder::RasterizePresentationSurface(composed.surfaces[i]).pixels)
                    throw std::runtime_error("soldier pose: replacement RGB differs from original");
                if (publication && actual[i] == this) *publication = std::move(replay);
            }
            if (substituted.poseReplacements) {
                for (const auto& layer : scene.layers) {
                    if (!layer.pose) continue;
                    static std::atomic<uint64_t> poseScene{0};
                    const auto identity = layer.pose->origin.soldier.scene;
                    if (poseScene.exchange(identity) != identity)
                        std::fprintf(stderr, "SOLDIER_POSE: verified replacement scene=%llu\n",
                            static_cast<unsigned long long>(identity));
                    break;
                }
            }
        }
        static std::atomic<bool> announced{false};
        if (!announced.exchange(true))
            std::fprintf(stderr, "MISSION_LAYER_AUDIT: verified real producer interval\n");
        return scene;
    }
    bool PresentRecordedMission(cSurface* other) {
        if (!MissionPublicationEnabled()) return false;
        const auto recording = std::atomic_load(&mMissionAudit);
        bool compatible = bool(recording);
        if (recording) {
            std::lock_guard<std::mutex> lock(recording->mutex);
            for (const auto& source : recording->scene.destinations) {
                const auto& initial = source.initial;
                const cSurface* surface = initial.destination == mPresentationDestination ? this : other;
                if (!surface || surface->isLoadedImage() || !initial.backing.pixels ||
                    !surface->PresentationDestinationMatches(initial.destination,
                        initial.backing.width, initial.backing.height, initial.backing.stride,
                        initial.backing.pixels->size()) ||
                    surface->mWidth != initial.indexed.width ||
                    surface->mHeight != initial.indexed.height)
                    compatible = false;
            }
        }
        if (!compatible) {
            // Discard both aliases before the classic fallback, including same-size replacement.
            BeginMissionAudit(other, false);
            static std::atomic<bool> announced{false};
            if (!announced.exchange(true))
                std::fprintf(stderr, "MISSION_LAYER_PRESENT: classic fallback (missing or incompatible interval)\n");
            return false;
        }
        openfodder::PresentationTarget target;
        VerifyMissionAudit(other, &target); // Divergences must propagate; never hide them in fallback.
        if (!ApplyPresentation(target))
            throw std::runtime_error("mission publication: destination changed after verification");
        static std::atomic<bool> announced{false};
        if (!announced.exchange(true))
            std::fprintf(stderr, "MISSION_LAYER_PRESENT: published verified orders\n");
        return true;
    }
    openfodder::PresentationSurface CapturePresentation() const;
    bool isLoadedImage() const { return mIsLoadedImage; }
    bool CommitPauseBacking(const openfodder::PausePresentation& scene);
    bool ApplyPresentation(const openfodder::PresentationTarget& target);
    openfodder::IndexedLayer CaptureIndexedLayer() const;
    openfodder::RGBLayer CaptureRGBLayer() const;
    IndexedSurfaceState CaptureIndexedState() const;
    openfodder::SurfaceDraw CaptureDraw(int16 pSkipX = 16, int16 pSkipY = 16) const;
	void			surfaceSetToPalette();
	void			surfaceSetToPaletteNew();
					cSurface( size_t pWidth, size_t pHeight );
					cSurface( const cDimension& pDimension );
					~cSurface();

	void			clearBuffer(size_t pColor = 0);

	void			draw(const int16 pSkipX = 16, const int16 pSkipY = 16);						// Draw image to SDL Surface
	void			copyFrom(const cSurface* pFrom);
	void            mergeFrom(const cSurface* pFrom);
    void            mergeSurfaceBuffer(const cSurface* pFrom);

	bool            LoadPng(const std::string &pFile);

	void			Save();
	void			Restore();

	void			palette_SetToBlack();
	bool			palette_FadeTowardNew();
	void			palette_SetFromNew();

	void			paletteSet( cPalette* pPalette, uint32 pColorID = 0, uint32 pColors = g_MaxColors, bool pUseNow = false );

	void			paletteNew_SetToBlack();
	void			paletteNew_SetDimmed(uint8 pScale);

	inline SDL_Surface* GetSurface() const { return mSDLSurface; }
	inline SDL_Texture* GetTexture() const { return mTexture; };
	inline uint8*		GetSurfaceBuffer() const { return mSurfaceBuffer; }
	inline size_t		GetSurfaceBufferSize() const { return mSurfaceBufferSize; }

	inline size_t		GetWidth() const { return mWidth; }
	inline size_t		GetHeight() const { return mHeight; }

	inline bool			isPaletteAdjusting() const { return mPaletteAdjusting; }
    inline void         resetPaletteAdjusting() { mPaletteAdjusting = false; }
};
