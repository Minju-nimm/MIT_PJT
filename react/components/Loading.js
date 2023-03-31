import React from 'react';
import {Background, LoadingText} from './Styles';
import Spinner from "../images/loadingImg/Double Ring-1s-200px.gif";

export default () => {
  return (
    <Background>
      <div width="5%"><img src={Spinner} alt="로딩중" /></div>
      <LoadingText>잠시만 기다려 주세요.</LoadingText>
    </Background>
  );
};