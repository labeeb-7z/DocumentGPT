import React, { useState } from "react";
import Chatbox from "./chatbox";

const Summary = () => {
  const [text, setText] = useState("");

  const handleData = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("../api/Summary_trial.js", {
        method: "GET",
        body: formData,
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <Chatbox handleData={handleData} />
    </div>
  );
};

export default Summary;
