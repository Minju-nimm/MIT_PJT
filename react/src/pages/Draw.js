import React, { useRef, useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom'
import axios from "axios"; // 플라스크에 요청하는 코드의 모듈
import { useDispatch } from "react-redux";


// 이미지 가져오기
import drawimg from '../images/drawImg/draw_button.png'
import eraser from '../images/drawImg/eraser_button.png'
import clear from '../images/drawImg/clear_button.png'
import post from '../images/drawImg/post_button.png'
import sketchBook from '../images/drawImg/sketchbook.png'


const Draw = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const canvasRef = useRef(null);
  const [getCtx, setGetCtx] = useState(null);
  const [painting, setPainting] = useState(false);
  const [tool, setTool] = useState("pen");

   // End: 변수지정----------------------------------------------------------------------------




   useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    canvas.width = window.innerWidth * 0.589;
    canvas.height = window.innerHeight * 0.59;
    const ctx = canvas.getContext("2d");
    const size = Math.min(canvas.width, canvas.height) / 20; // 포인터 크기를 계산함
    ctx.lineWidth = size; // 포인터 크기
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.strokeStyle = "#000000"; // 그림 그려질때 색상
    setGetCtx(ctx);
  }, [canvasRef]);
  
  const clearCanvas = () => {
    if (!canvasRef.current) return; // canvasRef가 null일 때는 함수를 종료함
    const ctx = canvasRef.current.getContext("2d");
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
  };
  // End: clearCanvas----------------------------------------------------------------------------


  const handleTouchStart = e => { // 터치라는 이벤트가 발생이 되면 그 터치 좌표를 인식하게하고 인식된 곳에 그림을 그리게 해줌
    const mouseX = e.touches[0].clientX - canvasRef.current.offsetLeft; // 터치 이벤트 발생 했을때 좌표값X
    const mouseY = e.touches[0].clientY - canvasRef.current.offsetTop;  // 터치 이벤트 발생 했을때 좌표값Y
    setPainting(true); // 그림그리기가 시작되었음을 알리는 코드
    draw(mouseX, mouseY); // 시작이 되었으니 그리라는 코드 draw 함수 호출
  };
  // End: handleTouchStart----------------------------------------------------------------------------
  

  const handleTouchEnd = e => { // 터치 이벤트가 종료 되면 painting 상태 변수 값을 false로 변경하고, 현재 그리고 있는 그림의 경로를 담기
    setPainting(false); // 그림그리기가 종료되었음을 알리는 코드
    getCtx.closePath(); // 메서드는 현재 경로의 마지막 점과 처음 점을 연결하여 경로를 닫습니다. 이 때, 마지막 점과 처음 점 사이에 라인이 그려지지 않습니다. 따라서, 이 메서드는 경로를 닫아서 완성된 도형을 그리는 데 사용
  };
  // End: handleTouchEnd----------------------------------------------------------------------------


  const handleTouchMove = e => {// 터치 이벤트가 종료 되면 painting 상태 변수 값을 false로 변경하고, 현재 그리고 있는 그림의 경로를 담기
    e.preventDefault(); // 다른 이벤트가 발생하는걸 막기
    const mouseX = e.touches[0].clientX - canvasRef.current.offsetLeft; // 터치 이벤트 발생 했을때 좌표값X
    const mouseY = e.touches[0].clientY - canvasRef.current.offsetTop;  // 터치 이벤트 발생 했을때 좌표값Y
    draw(mouseX, mouseY); // 시작이 되었으니 그리라는 코드 draw 함수 호출
  };
  // End: handleTouchMove----------------------------------------------------------------------------


  
  const draw = async (x, y, isEnd = false) => { // 그림이 그려지는 코드 tool이 pen이면 그림이 그려지고 eraser면 그림이 지워짐 실제로 그림이 그려지는 함수가 이거임
    if (!painting) {
      getCtx.beginPath();
      getCtx.moveTo(x, y);
    } else {
      if (tool === "pen") {
        getCtx.lineTo(x, y);
        getCtx.stroke();
      } else if (tool === "eraser") {
        getCtx.globalCompositeOperation = "destination-out";//내가 터치하는 부분이 색이 나오는게 아니고 지워지게
        getCtx.lineWidth = Math.min(canvasRef.current.width, canvasRef.current.height) / 20; // 지우개 크기
        getCtx.lineTo(x, y);
        getCtx.stroke();
        getCtx.globalCompositeOperation = "source-over";
      }
    }
  };
  // End: draw----------------------------------------------------------------------------


  
  const drawFn = e => { // 마우스 이벤트가 발생했을때 호출되는 함수 마우스와 터치를 다르게 생각하셔야합니당
    const mouseX = e.nativeEvent.offsetX; //마우스 위치 X
    const mouseY = e.nativeEvent.offsetY; //마우스 위치 Y
    if (!painting) {
      getCtx.beginPath();
      getCtx.moveTo(mouseX, mouseY);
    } else {
      draw(mouseX, mouseY);
    }
  };
  // End: drawFn----------------------------------------------------------------------------

  const getDrawArea = (canvas) => {
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;
    const imageData = ctx.getImageData(0, 0, w, h);
    const pixels = imageData.data;
    let minX = w, minY = h, maxX = 0, maxY = 0;
  
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const pixelIndex = (y * w + x) * 4;
        if (pixels[pixelIndex + 3] > 0) {
          minX = Math.min(minX, x);
          minY = Math.min(minY, y);
          maxX = Math.max(maxX, x);
          maxY = Math.max(maxY, y);
        }
      }
    }
    
    const padding =40;
    return [
      Math.max(0, minX - padding),
      Math.max(0, minY - padding),
      Math.min(w, maxX + padding) - Math.max(0, minX - padding),
      Math.min(h, maxY + padding) - Math.max(0, minY - padding),
    ];
  };
  
  // End: getDrawArea ----------------------------------------------------------------------------


  const handleClick = async () => { //post 버튼을 눌렀을때 발생하는 코드들입니다.
    // 캔버스와 크기가 같은 새로운 캔버스를 생성합니다. 이미지 인식을 좋게 하기 위해 새로운 캔버스에 담을 코드들
    const canvas = canvasRef.current;
    const [x, y, w, h] = getDrawArea(canvas);
    const canvasResized = document.createElement("canvas");
    canvasResized.width = w;
    canvasResized.height = h;
    const context = canvasResized.getContext("2d"); 
    
    // 원본 캔버스에서 그려진 영역을 가져와서 새로운 캔버스에 그립니다.
    context.drawImage(canvas, x, y, w, h, 0, 0, w, h);

    // 이미지 데이터를 플라스크로 보내는 코드 시작 -------------------
    // 새로운 캔버스 이미지 데이터를 base64 문자열로 추출합니다.
    const imageData = canvasResized.toDataURL("image/png", { colorSpaceConversion: "none" });
    const blob = await new Promise(resolve => canvasResized.toBlob(resolve, 'image/png'));
    const imageUrl = URL.createObjectURL(blob);
    // HTTP POST 요청 데이터를 생성합니다.
    const data = { "image": imageData };
    const response = await axios.post('여기에 서버 주소를 넣어야함', data); // http://101.101.101.101:80


    dispatch({ type: "CLEARRESULT" });
    dispatch({type:"IMAGEDATA",payload:{image:imageUrl,result:response.data}})
    navigate('/popup')
    clearCanvas();
  };
  // End: handleClick----------------------------------------------------------------------------
  






        
  return (
    <div className='draw_container'>
      <ul className='buttons'>
          <li><button className='draw_button' onClick={() => setTool("pen")}><img src={drawimg} alt='연필 버튼'/></button></li>
          <li><button className='eraser_button' onClick={() => setTool("eraser")}><img src={eraser} alt='지우개 버튼'/></button></li>
          <li><button className='clear_button' onClick={clearCanvas}><img src={clear} alt='휴지통 버튼'/></button></li>
          <li><button className='post_button' onClick={handleClick}><img src={post} alt='그려진 이미지가 뭔지 확인하는 버튼'/></button></li>
      </ul>
      <div className='canvas_wrap'>
        <img className='sketch' src={sketchBook} alt='스케치북 이미지'></img>
        <canvas
          className="canvas"
          ref={canvasRef}
          onMouseDown={() => setPainting(true)}
          onMouseUp={() => setPainting(false)}
          onMouseMove={e => drawFn(e)}
          onMouseLeave={() => setPainting(false)} // onMouseLeave 이벤트 추가
          
          onTouchStart={handleTouchStart}
          onTouchEnd={handleTouchEnd}
          onTouchMove={handleTouchMove}
        >
        </canvas>
      </div>
    </div>
  )
}


export default Draw
