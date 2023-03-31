import React, { useState, useEffect, useRef } from "react";
import cursorImg from "../images/cursorImg/pencil.svg"

const Cursor = (props) => {
  const { mousePos } = props;
  const cursorRef = useRef(null);
  const [cursorHeight, setCursorHeight] = useState(0);

  useEffect(() => {
    if (cursorRef.current) {
      setCursorHeight(cursorRef.current.offsetHeight);
    }
  }, []);

  const x = mousePos.x;
  const y = mousePos.y - cursorHeight + window.scrollY -148;

  return (
    <div
      ref={cursorRef}
      className="cursor"
      style={{
        position: "absolute",
        
        top: y + "px",
        left: x + "px",
        backgroundRepeat: "no-repeat",
        zIndex: "9999",
      }}
    ><img src={cursorImg}/></div>
  );
};

export default Cursor;
