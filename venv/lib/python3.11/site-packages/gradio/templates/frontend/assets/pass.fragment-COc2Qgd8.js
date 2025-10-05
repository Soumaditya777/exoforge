import{j as r}from"./index-zOiM5ifH.js";import"./index-DW22crb7.js";import"./svelte/svelte.js";const e="passPixelShader",a=`varying vec2 vUV;uniform sampler2D textureSampler;
#define CUSTOM_FRAGMENT_DEFINITIONS
void main(void) 
{gl_FragColor=texture2D(textureSampler,vUV);}`;r.ShadersStore[e]||(r.ShadersStore[e]=a);const s={name:e,shader:a};export{s as passPixelShader};
//# sourceMappingURL=pass.fragment-COc2Qgd8.js.map
