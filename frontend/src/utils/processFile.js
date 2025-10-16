import axios from 'axios';

export const uploadFile = async (file) => {

  const formData = new FormData();
  const API_URL = 'http://127.0.0.1:8000/upload';
  
  formData.append("file", file);



  try{

    console.log('File being sent:', file);
    console.log('File name:', file?.name);
    console.log('File type:', file?.type);
   
    const response = await axios.post(API_URL, formData);
    const data = response.data
    
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