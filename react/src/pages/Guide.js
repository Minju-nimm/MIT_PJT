import React from 'react';
import { useNavigate } from 'react-router-dom';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";// 폰트어썸 모듈 이것도 찾아보시면 좋아요
import { faPlay} from "@fortawesome/free-solid-svg-icons";

import guideImg from '../images/guideImg/guideImg.png';
import mainGuideButton from '../images/guideImg/main_guide_button.png'

const Guide = () => {
  const navigate = useNavigate();

  const goToDraw = () => {
    navigate('/draw')
};

const mainGoToDraw = () => {
  navigate('/draw');
  setTimeout(() => {
    window.scrollTo(0, 0);
  }, 0);
};

  return (
    <div className="guide_container">
      <button className='sketch_page_button' onClick={goToDraw}>바로 그림 그리러 가기 <FontAwesomeIcon icon={faPlay} /></button>
      <div className="guide_img">
        <img src={guideImg} alt="guide"/>
      </div>
      <button className='main_sketch_page_button' onClick={mainGoToDraw}><img src={mainGuideButton}/></button>
    </div>
  );
};

export default Guide;
