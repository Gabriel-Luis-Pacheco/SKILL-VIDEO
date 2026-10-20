/**
 * Original experimental motion. No logos, made-up UI or external assets.
 * 7 seconds, 30 fps, 1080x1920. Silent: sound designed separately.
 * Not a verified rendered commercial.
 */
import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

const background = '#0D1114';
const paper = '#F4F0E7';
const signal = '#E7B260';
const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

export const VideoOSMotionStudy: React.FC = () => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const arrival = spring({frame:f, fps, config:{mass:1.5, damping:24, stiffness:105}});
  const moveX = interpolate(f, [12,44], [-width*.46, 0], {...clamp,easing:Easing.out(Easing.cubic)});
  const compression = interpolate(f,[35,44,50,58],[1,.83,1.05,1],clamp);
  const relation = interpolate(f,[68,118],[0,1],{...clamp,easing:Easing.inOut(Easing.cubic)});
  const title = interpolate(f,[119,153],[0,1],{...clamp,easing:Easing.out(Easing.cubic)});
  const final = interpolate(f,[177,199],[0,1],clamp);
  const cx = width/2, cy = height*.40;
  const left = cx-width*.22, right = cx+width*.22;
  const path = 'M '+left+' '+(cy+25)+' C '+(cx-width*.10)+' '+(cy-120)+' '+(cx+width*.10)+' '+(cy+170)+' '+right+' '+(cy+25);
  const headingY = (1-title)*50;
  return (
    <AbsoluteFill style={{backgroundColor:background,color:paper,fontFamily:'Arial, Helvetica, sans-serif'}}>
      <div style={{position:'absolute',top:90,left:75,right:75,display:'flex',justifyContent:'space-between',fontSize:23,letterSpacing:4,opacity:.75}}>
        <span>FORMA</span><span>01 / 03</span>
      </div>
      <div style={{position:'absolute',left:cx-92,top:cy-92,width:184,height:184,borderRadius:96,
        border:'6px solid '+paper,backgroundColor:signal,boxShadow:'0 20px 55px rgba(0,0,0,.22)',
        transform:'translateX('+moveX+'px) scaleX('+compression+') scale('+(0.75+arrival*.25)+')'}} />
      <svg width={width} height={height} viewBox={'0 0 '+width+' '+height} style={{position:'absolute',inset:0}}>
        <path d={path} fill="none" stroke={paper} strokeWidth={7} strokeLinecap="round"
          pathLength={1} strokeDasharray={1} strokeDashoffset={1-relation} opacity={relation}/>
        <circle cx={left} cy={cy+25} r={25*relation} fill={paper} />
        <circle cx={right} cy={cy+25} r={25*relation} fill={paper} />
      </svg>
      <div style={{position:'absolute',left:65,right:65,top:height*.61,textAlign:'center',opacity:title,
        transform:'translateY('+headingY+'px)'}}>
        <div style={{fontSize:33,letterSpacing:7,fontWeight:500,opacity:.85}}>UMA IDEIA</div>
        <div style={{fontSize:87,lineHeight:1.04,letterSpacing:-4,fontWeight:800,marginTop:15}}>GANHA FORMA.</div>
      </div>
      <div style={{position:'absolute',bottom:110,left:78,right:78,height:2,backgroundColor:paper,opacity:final*.6}}/>
      <div style={{position:'absolute',bottom:61,left:78,fontSize:21,letterSpacing:2,opacity:final*.8}}>
        ESTUDO AUTORAL DE MOVIMENTO
      </div>
    </AbsoluteFill>
  );
};
