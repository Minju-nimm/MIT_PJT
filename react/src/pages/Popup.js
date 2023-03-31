import React, { useState, useEffect } from 'react';
import axios from "axios";

import { useSelector,useDispatch  } from 'react-redux';
import { useNavigate } from 'react-router-dom';

import popupImg from '../images/popupImg/popupImg.png'
import popupTrue from '../images/popupImg/popupTrue.png'
import popupFalse from '../images/popupImg/popupFalse.png'

import Loading from '../components/Loading';


const Popup = () => {
    const navigate = useNavigate();

    const result = useSelector(state => state.result);
    const [imageUrl, setImageUrl] = useState('');
    const [name, setname] = useState('');
    const [loading, setLoading] = useState(false);


    const dispatch = useDispatch();

    const goToDraw = () => {
        navigate('/draw')
    };




    
    useEffect(() => {
        const url = result[0].image;
        const resultName = result[0].result.prediction;
        setImageUrl(url);
        setname(resultName);
        }, [result]);
    
        
        const handleButtonClick = async () => {
            setLoading(true);
            try {
                // POST 요청 보내기 - 이미지 - 스토리
                const storyResponse = await axios.post('여기에 서버 주소 넣어야함');// http://101.101.101.101:80
                // const story = storyResponse.data.story;
                let story = "";
                for (let i=0; i<storyResponse.data.length; i++) {
                    if (storyResponse.data[i]) { // 현재 요소의 값이 존재하는 경우에만 문자열 추가
                    story += storyResponse.data[i];
                    console.log(story);
                    } else {
                    break; // 요소의 값이 없는 경우에는 반복문 종료
                    }
                }
                dispatch({ type: "CLEARSTORY" });
                dispatch({type:"STORYDATA",payload:{story:story}})
                
                const response = await axios.post('여기에 서버 주소 넣어야함', {}, { responseType: 'arraybuffer' });// http://101.101.101.101:80
                const blob = new Blob([response.data], { type: 'image/png' });
                const fairytaleImg = URL.createObjectURL(blob);

                dispatch({ type: "CLEARFAIRYTALE" });
                dispatch({type:"FAIRYTALE",payload:{fairytaleImg:fairytaleImg}})
                navigate('/fairytale')
        
            } catch (error) {
                console.error(error);  
            }
            setLoading(false); // 로딩 화면 끄기
        };
        
  return (
    <div>{loading ? <Loading /> : null}
    <div className='popup_container'>
        <div className='popup_img_container'>
            <img className='popup_img_bg' src={popupImg} alt='이미지 확인 그림'/>
            <div className='popup_img'>
                {imageUrl ? <img src={imageUrl} alt='그림' /> : null}
            </div>
        </div>
        
        <div className='popup_contents_container'>
            <div className='popup_contents'>
                <div>내가 그린 <span>“<strong style={{ fontSize: name.length <= 3 ? "5vw" : "3vw" }}>{ name }</strong>”</span> 그림</div>
                <ul>
                    <li>· 마음에 들지 않으면 새로 그릴 수 있어요!</li>
                    <li>· <strong >“{name}”</strong>에 대한 동화를 만들어 볼까요?</li>
                </ul>
            </div>
            <div className='popup_buttons'>
                <button onClick={handleButtonClick}><img src={popupTrue} alt='팝업 true 버튼'></img></button>
                <button onClick={goToDraw}><img src={popupFalse} alt='팝업 false 버튼'></img></button>
            </div>
        </div>
        </div>
    </div>
  )
}

export default Popup