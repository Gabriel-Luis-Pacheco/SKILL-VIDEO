import React from 'react';
import {Composition} from 'remotion';
import {VideoOSMotionStudy} from './Video';
export const RemotionRoot: React.FC = () =>
  <Composition id="VideoOSMotionStudy" component={VideoOSMotionStudy}
    fps={30} durationInFrames={210} width={1080} height={1920} />;
