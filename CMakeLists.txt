cmake_minimum_required(VERSION 3.10.0)

if (POLICY CMP0025)
  cmake_policy(SET CMP0025 NEW)
endif ()

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    message(STATUS "No build type selected, default to Release.")
    set(CMAKE_BUILD_TYPE "Release")
endif()

project(openfodder VERSION 1.5.4 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)
option(OPENFODDER_ENABLE_FFMPEG "Enable FFmpeg intro video playback" OFF)
option(OPENFODDER_AUTO_FFMPEG "Auto-enable FFmpeg when found (non-Windows)" ON)

if(MSVC)
    # Enable Hot Reload (Edit and Continue) for Debug builds.
    set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<CONFIG:Debug>,EditAndContinue,ProgramDatabase>")
    add_compile_options($<$<CONFIG:Debug>:/ZI>)
    add_link_options($<$<CONFIG:Debug>:/INCREMENTAL>)
endif()

if(EMSCRIPTEN)
    set(OPENFODDER_EMSCRIPTEN ON)
else()
    find_package(Threads REQUIRED)
endif()

if(EMSCRIPTEN)
elseif(WIN32)
    include(FetchContent)

    set(SDL_INSTALL OFF CACHE BOOL "" FORCE)
    set(SDL_SHARED ON CACHE BOOL "" FORCE)
    set(SDL_STATIC OFF CACHE BOOL "" FORCE)
    set(SDL_TESTS OFF CACHE BOOL "" FORCE)

    set(SDLMIXER_VENDORED ON CACHE BOOL "" FORCE)
    set(SDLMIXER_MOD_XMP ON CACHE BOOL "" FORCE)
    set(SDLMIXER_MOD_XMP_LITE ON CACHE BOOL "" FORCE)
    set(SDLMIXER_MOD_XMP_SHARED OFF CACHE BOOL "" FORCE)
    set(SDLMIXER_TESTS OFF CACHE BOOL "" FORCE)
    set(SDLMIXER_INSTALL OFF CACHE BOOL "" FORCE)

    set(SDL3_GIT_TAG "release-3.4.0")
    set(SDL3_MIXER_GIT_TAG "3045b35335113e5e5ba258858cb403d8803bfbeb")

    FetchContent_Declare(
        SDL3
        GIT_REPOSITORY https://github.com/libsdl-org/SDL.git
        GIT_TAG ${SDL3_GIT_TAG}
        GIT_SHALLOW FALSE
    )

    FetchContent_Declare(
        SDL3_mixer
        GIT_REPOSITORY https://github.com/libsdl-org/SDL_mixer.git
        GIT_TAG ${SDL3_MIXER_GIT_TAG}
        GIT_SHALLOW FALSE
    )

    FetchContent_MakeAvailable(SDL3)
    FetchContent_MakeAvailable(SDL3_mixer)

    set(_sdl_mixer_compat_header "${CMAKE_CURRENT_LIST_DIR}/cmake/sdl3_mixer_compat.h")
    foreach(_sdl_mixer_target IN ITEMS SDL3_mixer SDL3_mixer-shared SDL3_mixer-static)
        if(TARGET ${_sdl_mixer_target})
            if(MSVC)
                target_compile_options(${_sdl_mixer_target} PRIVATE "/FI${_sdl_mixer_compat_header}")
            else()
                target_compile_options(${_sdl_mixer_target} PRIVATE "-include" "${_sdl_mixer_compat_header}")
            endif()
        endif()
    endforeach()
else()
    find_package(SDL3 CONFIG REQUIRED)
    find_package(SDL3_mixer CONFIG REQUIRED)
endif()

# Locate git binary to provide information to the build environment
find_package(Git)

if(GIT_FOUND)
# Define short commit hash.
    execute_process(
        COMMAND ${GIT_EXECUTABLE} rev-parse --short HEAD
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        OUTPUT_VARIABLE OPENFODDER_COMMIT_SHA1_SHORT
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_QUIET
    )
else()
# Fallback in case the git exe can't be found.
    set(OPENFODDER_COMMIT_SHA1_SHORT "deadbeef")
endif()

configure_file(cmake/gitver.hpp.in Source/gitver.hpp @ONLY)

file(GLOB_RECURSE GAMEENGINE_HEADERS "Source/*.hpp")
file(GLOB_RECURSE GAMEENGINE_SOURCE "Source/*.cpp")

source_group(TREE "${CMAKE_SOURCE_DIR}/Source" FILES ${GAMEENGINE_HEADERS} ${GAMEENGINE_SOURCE})

if(EMSCRIPTEN)
    list(FILTER GAMEENGINE_SOURCE EXCLUDE REGEX "Source/PC/Sound_PC2.cpp$")
    list(FILTER GAMEENGINE_SOURCE EXCLUDE REGEX "Source/PC/Sound_PC.cpp$")
    list(FILTER GAMEENGINE_SOURCE EXCLUDE REGEX "Source/Start.cpp$")
endif()

add_executable(openfodder ${GAMEENGINE_SOURCE} ${GAMEENGINE_HEADERS})

# Pure arithmetic boundary test: no SDL or game assets needed.
enable_testing()
find_package(Python3 COMPONENTS Interpreter QUIET)
if(Python3_Interpreter_FOUND)
    set(_presentation_fixture "${CMAKE_CURRENT_BINARY_DIR}/presentation_options_fixture.cpp")
    add_custom_command(OUTPUT "${_presentation_fixture}"
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_presentation_options.py"
                --emit "${_presentation_fixture}"
        DEPENDS tools/modernization/check_presentation_options.py
                tools/modernization/check_final_timer_equivalence.py
                Source/OptionsMenu.cpp Source/OptionsMenu.hpp Source/Parameters.cpp
                Source/Parameters.hpp Source/Window.cpp Source/Window.hpp
                Source/Utils/PresentationOptions.hpp Source/Utils/ini.hpp
        VERBATIM)
    add_executable(openfodder_presentation_tests "${_presentation_fixture}")
    target_include_directories(openfodder_presentation_tests PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/Source")
    add_test(NAME presentation_options_transaction COMMAND $<TARGET_FILE:openfodder_presentation_tests>)
    set(_font_fixture "${CMAKE_CURRENT_BINARY_DIR}/options_font_fixture.cpp")
    add_custom_command(OUTPUT "${_font_fixture}"
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_options_font.py"
                --emit "${_font_fixture}"
        DEPENDS tools/modernization/check_options_font.py
                tools/modernization/check_final_timer_equivalence.py
                tools/modernization/check_sprite_table_lengths.py
                Source/OptionsMenu.cpp Source/String.cpp Source/GUI_Element.cpp
                Source/Sprites/Sprite_Core.cpp Source/FontData.cpp
                Source/PC/SpriteData_PC.hpp Source/Amiga/SpriteData_Amiga.hpp
        VERBATIM)
    add_executable(openfodder_options_font_tests "${_font_fixture}")
    target_include_directories(openfodder_options_font_tests PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/Source")
    add_test(NAME options_confirmation_font COMMAND $<TARGET_FILE:openfodder_options_font_tests>)
endif()
# Isolated HD pose pilot: generates derivatives from the preserved original PNG.
add_executable(openfodder_art_builder tools/modernization/build_soldier_art.cpp)
target_include_directories(openfodder_art_builder PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/Source")
foreach(_density IN ITEMS 8 12)
    add_custom_command(OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/c01_${_density}.hpp"
        COMMAND $<TARGET_FILE:openfodder_art_builder>
            "${CMAKE_CURRENT_SOURCE_DIR}/assets/modernization/soldier-c01/source.png"
            "${CMAKE_CURRENT_BINARY_DIR}/c01_${_density}.hpp" ${_density}
        DEPENDS openfodder_art_builder assets/modernization/soldier-c01/source.png
        VERBATIM)
endforeach()
add_executable(openfodder_art_hd_tests tools/modernization/test_soldier_art_hd.cpp
    "${CMAKE_CURRENT_BINARY_DIR}/c01_8.hpp" "${CMAKE_CURRENT_BINARY_DIR}/c01_12.hpp")
target_include_directories(openfodder_art_hd_tests PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/Source" "${CMAKE_CURRENT_BINARY_DIR}")
add_test(NAME soldier_art_hd_isolated COMMAND $<TARGET_FILE:openfodder_art_hd_tests>)
# Shared generated assets are built once before either consumer compiles.
add_dependencies(openfodder openfodder_art_hd_tests)
target_include_directories(openfodder PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")
add_executable(openfodder_art_sdl_tests tools/modernization/test_soldier_art_sdl.cpp)
add_dependencies(openfodder_art_sdl_tests openfodder_art_hd_tests)
target_include_directories(openfodder_art_sdl_tests PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/Source" "${CMAKE_CURRENT_BINARY_DIR}")
target_link_libraries(openfodder_art_sdl_tests PRIVATE SDL3::SDL3)
add_test(NAME soldier_art_sdl_transaction COMMAND $<TARGET_FILE:openfodder_art_sdl_tests>)
include(tools/modernization/soldier_batch_assets.cmake)
if(Python3_Interpreter_FOUND)
    set(_hd_window_fixture "${CMAKE_CURRENT_BINARY_DIR}/hd_window_fixture.cpp")
    add_custom_command(OUTPUT "${_hd_window_fixture}"
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/build_hd_window_fixture.py" --emit "${_hd_window_fixture}"
        DEPENDS tools/modernization/build_hd_window_fixture.py Source/WindowHD.cpp
            docs/modernization/evidence/soldier-coverage-matrix.json
            docs/modernization/evidence/soldier-catalog.json VERBATIM)
    add_executable(openfodder_hd_window_tests "${_hd_window_fixture}")
    add_dependencies(openfodder_hd_window_tests openfodder_art_sdl_tests)
    target_include_directories(openfodder_hd_window_tests PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/Source" "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization" "${CMAKE_CURRENT_BINARY_DIR}")
    target_link_libraries(openfodder_hd_window_tests PRIVATE SDL3::SDL3)
    add_test(NAME soldier_hd_window_lifecycle COMMAND $<TARGET_FILE:openfodder_hd_window_tests>)
    add_test(NAME soldier_ordered_coverage COMMAND "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_ordered_coverage_integration.py"
        --exe $<TARGET_FILE:openfodder_hd_window_tests>)
    add_executable(openfodder_external_asset_tests "${_hd_window_fixture}")
    target_compile_definitions(openfodder_external_asset_tests PRIVATE OPENFODDER_EXTERNAL_ASSET_FIXTURE)
    add_dependencies(openfodder_external_asset_tests openfodder_hd_window_tests)
    target_include_directories(openfodder_external_asset_tests PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/Source" "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization" "${CMAKE_CURRENT_BINARY_DIR}")
    target_link_libraries(openfodder_external_asset_tests PRIVATE SDL3::SDL3)
    add_test(NAME soldier_external_assets COMMAND "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_ordered_asset_integration.py"
        --exe $<TARGET_FILE:openfodder_external_asset_tests>)
    add_executable(openfodder_ordered_asset_builder tools/modernization/build_ordered_soldier_asset.cpp)
    target_include_directories(openfodder_ordered_asset_builder PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/Source")
    add_test(NAME soldier_external_asset_export COMMAND "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_ordered_asset_builder.py"
        --exe $<TARGET_FILE:openfodder_ordered_asset_builder>)
    add_test(NAME soldier_walk_art_review COMMAND "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_walk_art_review.py"
        --exe $<TARGET_FILE:openfodder_external_asset_tests>
        --c01-builder $<TARGET_FILE:openfodder_art_builder>
        --batch-builder $<TARGET_FILE:openfodder_batch_builder>
        --asset-builder $<TARGET_FILE:openfodder_ordered_asset_builder>)
    add_test(NAME soldier_walk24_art COMMAND "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_walk24_art.py"
        --exe $<TARGET_FILE:openfodder_external_asset_tests>
        --c01-builder $<TARGET_FILE:openfodder_art_builder>
        --batch-builder $<TARGET_FILE:openfodder_batch_builder>
        --asset-builder $<TARGET_FILE:openfodder_ordered_asset_builder>)
    set(_aim_selector_fixture "${CMAKE_CURRENT_BINARY_DIR}/aim_selector_fixture.cpp")
    add_custom_command(OUTPUT "${_aim_selector_fixture}"
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_aim_selection.py"
            --emit "${_aim_selector_fixture}"
        DEPENDS tools/modernization/check_aim_selection.py tools/modernization/check_final_timer_equivalence.py
            Source/Sprites.cpp Source/Sprites/Sprite_Troop.cpp VERBATIM)
    add_executable(openfodder_aim_selector_tests "${_aim_selector_fixture}")
    add_test(NAME soldier_aim_original_selection COMMAND $<TARGET_FILE:openfodder_aim_selector_tests>)
    add_test(NAME soldier_aim_art COMMAND "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_aim_art.py"
        --exe $<TARGET_FILE:openfodder_external_asset_tests>
        --selector-exe $<TARGET_FILE:openfodder_aim_selector_tests>
        --c01-builder $<TARGET_FILE:openfodder_art_builder>
        --batch-builder $<TARGET_FILE:openfodder_batch_builder>
        --asset-builder $<TARGET_FILE:openfodder_ordered_asset_builder>)
    set(_grenade_selector_fixture "${CMAKE_CURRENT_BINARY_DIR}/grenade_selector_fixture.cpp")
    add_custom_command(OUTPUT "${_grenade_selector_fixture}"
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_grenade_selection.py"
            --emit "${_grenade_selector_fixture}"
        DEPENDS tools/modernization/check_grenade_selection.py tools/modernization/check_aim_selection.py
            tools/modernization/check_final_timer_equivalence.py ${GAMEENGINE_SOURCE} ${GAMEENGINE_HEADERS} VERBATIM)
    add_executable(openfodder_grenade_selector_tests "${_grenade_selector_fixture}")
    add_test(NAME soldier_grenade_original_selection COMMAND $<TARGET_FILE:openfodder_grenade_selector_tests>)
    add_test(NAME soldier_grenade_art COMMAND "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_grenade_art.py"
        --exe $<TARGET_FILE:openfodder_external_asset_tests>
        --selector-exe $<TARGET_FILE:openfodder_grenade_selector_tests>
        --c01-builder $<TARGET_FILE:openfodder_art_builder>
        --batch-builder $<TARGET_FILE:openfodder_batch_builder>
        --asset-builder $<TARGET_FILE:openfodder_ordered_asset_builder>)
    set(_rocket_selector_fixture "${CMAKE_CURRENT_BINARY_DIR}/rocket_selector_fixture.cpp")
    add_custom_command(OUTPUT "${_rocket_selector_fixture}"
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_rocket_selection.py"
            --emit "${_rocket_selector_fixture}"
        DEPENDS tools/modernization/check_rocket_selection.py tools/modernization/check_aim_selection.py
            tools/modernization/check_final_timer_equivalence.py tools/modernization/audit_contract.py
            tools/modernization/check_sprite_table_lengths.py ${GAMEENGINE_SOURCE} ${GAMEENGINE_HEADERS} VERBATIM)
    add_executable(openfodder_rocket_selector_tests "${_rocket_selector_fixture}")
    add_test(NAME soldier_rocket_original_selection COMMAND $<TARGET_FILE:openfodder_rocket_selector_tests>)
    add_test(NAME soldier_rocket_art COMMAND "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_rocket_art.py"
        --exe $<TARGET_FILE:openfodder_external_asset_tests>
        --selector-exe $<TARGET_FILE:openfodder_rocket_selector_tests>
        --c01-builder $<TARGET_FILE:openfodder_art_builder>
        --batch-builder $<TARGET_FILE:openfodder_batch_builder>
        --asset-builder $<TARGET_FILE:openfodder_ordered_asset_builder>)
    add_executable(openfodder_aim_reference tools/modernization/rekey_aim_reference.cpp)
    target_include_directories(openfodder_aim_reference PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/Source" "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization")
    add_executable(openfodder_native_walk_renderer tools/modernization/render_walk_native.cpp)
    add_executable(openfodder_native_walk_snapshot_test tools/modernization/test_native_walk_snapshot.cpp)
    foreach(_native_target IN ITEMS openfodder_native_walk_renderer openfodder_native_walk_snapshot_test)
        target_include_directories(${_native_target} PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/Source")
    endforeach()
    add_test(NAME soldier_native_walk_snapshot COMMAND "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/check_native_walk_snapshot.py"
        --fixture $<TARGET_FILE:openfodder_native_walk_snapshot_test>
        --renderer $<TARGET_FILE:openfodder_native_walk_renderer>)
    if(WIN32)
        foreach(_hd_test IN ITEMS openfodder_art_sdl_tests openfodder_hd_window_tests openfodder_external_asset_tests)
            add_custom_command(TARGET ${_hd_test} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_FILE:SDL3::SDL3> $<TARGET_FILE_DIR:${_hd_test}> VERBATIM)
        endforeach()
    endif()
endif()


add_executable(openfodder_direction_tests tools/modernization/test_direction_lut.cpp)
add_executable(openfodder_sprite_frame_tests tools/modernization/test_sprite_frame_bounds.cpp)
add_executable(openfodder_index_layout_tests tools/modernization/test_index_layout.cpp)
add_executable(openfodder_endian_io_tests tools/modernization/test_endian_io.cpp)
add_executable(openfodder_rng_tests tools/modernization/test_rng_bit_exact.cpp)
add_executable(openfodder_signed_bits_tests tools/modernization/test_signed_bits.cpp)
add_test(NAME signed_bits_equivalence COMMAND $<TARGET_FILE:openfodder_signed_bits_tests>)
add_test(NAME pseudorandom_bit_exact COMMAND $<TARGET_FILE:openfodder_rng_tests>)
add_test(NAME endian_unaligned_reads COMMAND $<TARGET_FILE:openfodder_endian_io_tests>)
add_test(NAME squad_huffman_index_layout COMMAND $<TARGET_FILE:openfodder_index_layout_tests>)
add_test(NAME sprite_frame_bounds COMMAND $<TARGET_FILE:openfodder_sprite_frame_tests>)
add_test(NAME direction_lookup_bounds COMMAND $<TARGET_FILE:openfodder_direction_tests>)

if(WIN32)
    target_sources(openfodder PRIVATE
        "${CMAKE_SOURCE_DIR}/Projects/OpenFodder.rc"
        "${CMAKE_SOURCE_DIR}/Projects/resource.h")
endif()

if(MSVC)
    set_target_properties(openfodder PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/Run"
        RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_SOURCE_DIR}/Run"
        RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_SOURCE_DIR}/Run"
        RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO "${CMAKE_SOURCE_DIR}/Run"
        RUNTIME_OUTPUT_DIRECTORY_MINSIZEREL "${CMAKE_SOURCE_DIR}/Run")
    set_target_properties(openfodder PROPERTIES
        VS_DEBUGGER_WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/Run")
    set_property(DIRECTORY PROPERTY VS_STARTUP_PROJECT openfodder)
endif()

target_include_directories(openfodder PRIVATE
    Source
    ${CMAKE_CURRENT_BINARY_DIR}/Source)

target_compile_definitions(openfodder PRIVATE
    UNICODE
    _UNICODE
    _USE_MATH_DEFINES)

if (OPENFODDER_ENABLE_FFMPEG OR (OPENFODDER_AUTO_FFMPEG AND NOT WIN32))
    list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")
    find_package(FFmpeg)
    if (FFmpeg_FOUND)
        target_compile_definitions(openfodder PRIVATE OPENFODDER_ENABLE_FFMPEG)
        target_include_directories(openfodder PRIVATE ${FFMPEG_INCLUDE_DIRS})
        target_link_libraries(openfodder PRIVATE ${FFMPEG_LIBRARIES})
    elseif(OPENFODDER_ENABLE_FFMPEG)
        message(WARNING "FFmpeg not found; intro video playback disabled.")
    endif()
endif()

if(EMSCRIPTEN)
    target_compile_definitions(openfodder PRIVATE EMSCRIPTEN OPENFODDER_NO_MIXER)
    target_compile_options(openfodder PRIVATE "-sUSE_SDL=3")
    set_target_properties(openfodder PROPERTIES
        OUTPUT_NAME "OpenFodder"
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/RunE"
        SUFFIX ".html")
    target_link_options(openfodder PRIVATE
        "-sUSE_SDL=3"
        "-sALLOW_MEMORY_GROWTH=1"
        "-sASSERTIONS=1"
        "SHELL:--preload-file ${CMAKE_SOURCE_DIR}/Run@/")
else()
    target_link_libraries(openfodder PRIVATE SDL3::SDL3 SDL3_mixer::SDL3_mixer Threads::Threads)
endif()

if(WIN32)
    set(_runtime_dlls "")
    if(TARGET SDL3::SDL3)
        list(APPEND _runtime_dlls $<TARGET_FILE:SDL3::SDL3>)
    elseif(TARGET SDL3-shared)
        list(APPEND _runtime_dlls $<TARGET_FILE:SDL3-shared>)
    endif()

    if(TARGET SDL3_mixer::SDL3_mixer)
        list(APPEND _runtime_dlls $<TARGET_FILE:SDL3_mixer::SDL3_mixer>)
    elseif(TARGET SDL3_mixer-shared)
        list(APPEND _runtime_dlls $<TARGET_FILE:SDL3_mixer-shared>)
    endif()

    if(_runtime_dlls)
        add_custom_command(TARGET openfodder POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
                ${_runtime_dlls}
                "${CMAKE_SOURCE_DIR}/Run"
            COMMENT "Copy SDL runtime DLLs to output directory")
    endif()
    target_link_libraries(openfodder PRIVATE ws2_32)
endif()

# A2 internal ordered compositor; no commercial assets or SDL required.
add_executable(openfodder_ordered_soldier_tests tools/modernization/test_ordered_soldier_art.cpp)
target_include_directories(openfodder_ordered_soldier_tests PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/Source")
add_test(NAME soldier_ordered_composition COMMAND $<TARGET_FILE:openfodder_ordered_soldier_tests>)
if(Python3_Interpreter_FOUND)
    add_test(NAME soldier_coverage_matrix COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tools/modernization/test_soldier_coverage.py")
endif()

# A2 ordered SDL publisher contract; no production resolver or artwork implied.
add_executable(openfodder_ordered_sdl_tests tools/modernization/test_ordered_soldier_sdl.cpp)
target_include_directories(openfodder_ordered_sdl_tests PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/Source")
target_link_libraries(openfodder_ordered_sdl_tests PRIVATE SDL3::SDL3)
add_test(NAME soldier_ordered_sdl_transaction COMMAND $<TARGET_FILE:openfodder_ordered_sdl_tests>)
if(WIN32)
    add_custom_command(TARGET openfodder_ordered_sdl_tests POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_FILE:SDL3::SDL3> $<TARGET_FILE_DIR:openfodder_ordered_sdl_tests> VERBATIM)
endif()
