import axios from 'axios';

export const uploadFile = async (file) => {

  const formData = new FormData();
  const API_URL = 'http://127.0.0.1:8000/upload';
  
  formData.append("file", file);

  //metadata
  formData.append("title", "test video");

  try{
   
    const response = await axios.post(API_URL, formData);

    const data = await response.json();
    
    if ("Duration" in data){
    console.log(data.duration)}
    else{
    console.log("No data received");
    }

    return data;

  } catch (error) {
    console.log("Axios error:", error)
  }



}