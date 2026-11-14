// GPL-3.0-or-later.
int main(){size_t rejected=0,accepted=0;
 for(int w:{32,80,400})for(int h:{32,64})for(int padding:{0,3})for(bool loaded:{false,true})for(bool textured:{false,true}){
  pad=padding;cSurface source(w,h),other(w,h),text(w,h);
  fill(source,7,loaded);fill(other,11,loaded);fill(text,13,false);
  SDL_Texture texture;if(textured)source.mTexture=other.mTexture=&texture;
  const auto scene=source.CapturePresentation();
  auto target=openfodder::RasterizePresentationSurface(scene);
  const auto logicalBefore=logical(source);int before=updates;
  assert(source.ApplyPresentation(target));assert(updates==before+int(textured));
  assert(*source.CaptureRGBLayer().pixels==target.pixels);assert(logical(source)==logicalBefore);++accepted;
  // Same geometry, different destination identity must not be accepted.
  reject(other,target);++rejected;
  for(int mutation=0;mutation<9;++mutation){auto bad=target;
   switch(mutation){case 0:bad.width++;break;case 1:bad.height++;break;case 2:bad.stride++;break;
    case 3:bad.pixels.pop_back();break;case 4:bad.pixels.push_back(0);break;
    case 5:bad.destination.reset();break;case 6:bad.height=0;break;
    case 7:bad.width=std::numeric_limits<size_t>::max();break;
    case 8:bad.stride=std::numeric_limits<size_t>::max();break;}
   reject(source,bad);++rejected;
  }
  openfodder::PausePresentation paused{scene,text.CapturePresentation()};
  auto oldOther=allState(other);before=updates;
  assert(!other.CommitPauseBacking(paused));assert(allState(other)==oldOther);assert(before==updates);++rejected;
  const auto expected=openfodder::RasterizePausePresentation(paused);
  assert(source.CommitPauseBacking(paused));assert(before==updates);
  const auto after=openfodder::RasterizePresentationSurface(source.CapturePresentation());
  for(size_t i=0;i<after.pixels.size();++i)if(openfodder::PresentationKeepsBacking(scene,i))assert(after.pixels[i]==expected.background.pixels[i]);
  ++accepted;
  // Matching token but corrupted storage geometry/format rejects without writes.
  const int oldPitch=source.mSDLSurface->pitch;
  source.mSDLSurface->pitch=oldPitch-1;
  // allState interprets words, so use direct storage and logical checks here.
  auto rgb=*source.CaptureRGBLayer().pixels;before=updates;
  assert(!source.ApplyPresentation(target));assert(*source.CaptureRGBLayer().pixels==rgb);assert(before==updates);++rejected;
  source.mSDLSurface->pitch=oldPitch;source.mSDLSurface->format=2;
  reject(source,target);++rejected;source.mSDLSurface->format=1;
 }
 // Exact cSurface address reuse: retained old tokens must remain distinct.
 pad=0;alignas(cSurface) unsigned char storage[sizeof(cSurface)];
 auto* first=new(storage)cSurface(80,64);fill(*first,5,false);
 auto old=first->CapturePresentation();std::weak_ptr<const openfodder::PresentationDestination> weak=old.destination;
 auto oldTarget=openfodder::RasterizePresentationSurface(old);auto expected=oldTarget.pixels;
 first->~cSurface();auto* second=new(storage)cSurface(80,64);fill(*second,9,false);
 reject(*second,oldTarget);++rejected;
 assert(openfodder::RasterizePresentationSurface(old).pixels==expected);
 // Actual LoadPng storage replacement, first with identical geometry.
 auto beforeLoad=second->CapturePresentation();auto stale=openfodder::RasterizePresentationSurface(beforeLoad);
 assert(second->LoadPng("controlled-rgba"));reject(*second,stale);++rejected;
 auto fresh=second->CapturePresentation();auto freshTarget=openfodder::RasterizePresentationSurface(fresh);
 assert(second->ApplyPresentation(freshTarget));++accepted;
 // Same surface, changed dimensions and format; old captures still rasterize.
 pngWidth=96;pngHeight=65;pngBytes=3;
 assert(second->LoadPng("controlled-rgb"));
 reject(*second,freshTarget);++rejected;
 assert(openfodder::RasterizePresentationSurface(fresh).pixels==freshTarget.pixels);
 // No new RGB-word capture on 24-bit PNG: that path's capture is not supported.
 second->~cSurface();old={};oldTarget={};assert(weak.expired());
 std::cout<<"PASS: "<<accepted<<" accepted publications/backing commits, "<<rejected
 <<" rejected incompatible destinations; identity, dimensions, pitch, extents, format, address reuse and actual LoadPng replacement; no writes/uploads on rejection\n";
}
