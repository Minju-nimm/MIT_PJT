import styled from 'styled-components';

export const Background = styled.div`
  position: absolute;
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  background: #ffffffb7;
  z-index: 999;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;


export const LoadingImg = styled.img`
width: 30vw;
height: 50vh;
`;
export const LoadingText = styled.div`
  font: 1rem 'Noto Sans KR';
  text-align: center;
`;