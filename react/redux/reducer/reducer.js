let initialState = {
    result: [],
    story:"",
    fairytaleImg:""
  };
  
  function reducer(state = initialState, action) {
    switch (action.type) {

        case "CLEARRESULT":
            return {
                ...state,
                result: []
            };
        case "IMAGEDATA":
            return {
            ...state,
            result: [
                {
                image: action.payload.image,
                result: action.payload.result
                }
            ]
            };


        case "CLEARSTORY":
            return {
                ...state,
                story: ""
            };
        case "STORYDATA":
            return {
                ...state,
                story: action.payload.story
            };


        case "CLEARFAIRYTALE":
            return {
                ...state,
                fairytaleImg: ""
            };
        case "FAIRYTALE":
            return {
            ...state,
            fairytaleImg: action.payload.fairytaleImg
                
            
            };




    


      default:
        return { ...state };
    }
  }
  
  export default reducer;
  