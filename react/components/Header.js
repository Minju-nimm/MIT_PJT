import React from 'react'
import { useNavigate } from 'react-router-dom'


import logo from '../images/headerImg/logo.png'
import drawButton from '../images/headerImg/drawButton.png'
import guideButton from '../images/headerImg/guideButton.png'




const Header = () => {

    const navigate = useNavigate();
    const goToDraw = () => {
        navigate('/draw')
    };

    const goToGuide = () => {
        navigate('/')
    };

  return (
    <div className='header_container'>
            <h1><img className='logo' src={logo} alt='로고 이미지'/></h1>
            <ul>
                <li><button onClick={goToDraw}><img className='draw_button' src={drawButton} alt='스케치북 이동 버튼'/></button></li>
                <li><button onClick={goToGuide}><img className='guide_button' src={guideButton} alt='가이드 이동 버튼'/></button></li>
            </ul>
    </div>
  )
}

export default Header