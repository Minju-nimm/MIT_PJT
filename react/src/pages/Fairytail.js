import React, { useState, useEffect, useRef } from 'react';
import { useSelector } from 'react-redux';
import axios from "axios";


import img2 from '../images/fairytaleImg/result_img2.png'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";// 폰트어썸 모듈 이것도 찾아보시면 좋아요
import { faMusic } from "@fortawesome/free-solid-svg-icons";

const Fairytail = () => {
    const result = useSelector(state => state.result);
    const story = useSelector(state => state.story);
    const fairytale = useSelector(state => state.fairytaleImg);

    const [imageUrl, setImageUrl] = useState('');
    const [storyContents, setStoryContents] = useState('');
    const [fairytaleUrl, setFairytaleUrlUrl] = useState('');
    const voiceRef = useRef(null);
 
    useEffect(() => {
        const url = result[0].image;
        setImageUrl(url);
        }, [result]);

    useEffect(()=>{
        const contents = story;
        setStoryContents(contents)
    },[story])

    useEffect(()=>{
        const fairytaleImgResult = fairytale;
        setFairytaleUrlUrl(fairytaleImgResult)
    },[fairytale])

    const voiceButton = async ()=>{
        try {
        // POST 요청을 보내고, 서버로부터 응답을 받아옵니다.
        const voiceResponse = await axios.post('여기에 서버 주소를 넣어야함', {}, { responseType: 'blob' });// http://101.101.101.101:80
    
        // 받아온 데이터를 Blob 객체로 변환합니다.
        const voiceBlob = new Blob([voiceResponse.data], { type: 'audio/mpeg' });
    
        // Blob 객체를 Audio 객체에 넘겨줍니다.
        const voice = new Audio(URL.createObjectURL(voiceBlob));
        voiceRef.current = voice;
        } catch (error) {
            console.error(error);
        }
        voiceRef.current.play();
    }


  return (
    <div className='fairytail_container'>
        <div className='img_container'>
            {imageUrl ? <img src={fairytaleUrl} alt='동화책 이미지' /> : null}
        </div>

        <div className='story_container'>
            <div className='story'>
                <div className='draw_img'>
                    {imageUrl ? <img src={imageUrl} alt='내가 그린 그림' /> : null}
                </div>
                <div className='story_contents'><span>“</span>{storyContents} <span>”</span></div>
                <button className="voice" onClick={voiceButton}><div>음성 재생하기 <FontAwesomeIcon icon={faMusic} /></div></button>
            </div>
            <div className='story_img'>
                <div><img src={img2} alt="동화책 꾸미는 이미지"/></div>
            </div>
        </div>
    </div>
  )
}

export default Fairytail