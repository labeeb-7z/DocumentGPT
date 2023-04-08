import React from 'react'
import Typewriter from "typewriter-effect";

const Chatbox = ({ text }) => {
  return (
    <div className="bg-[#121416] m-3">
      {/* <button
        onClick={handleData}
        class="relative inline-flex items-start justify-start p-0.5 mb-2 mr-2 overflow-hidden text-sm font-medium text-white rounded-lg group bg-gradient-to-br from-green-400 to-blue-600 group-hover:from-green-400 group-hover:to-blue-600 hover:text-white focus:ring-4 focus:outline-none focus:ring-green-200"
      >
        <span class="relative px-5 py-2.5 transition-all ease-in duration-75 bg-[#121416] rounded-md group-hover:bg-opacity-0">
          Process
        </span>
      </button> */}
      <div className="bg-slate-800 p-7">
        <Typewriter
          options={{
            strings: [
                `${text}`,
            ],
            autoStart: true,
            loop: true,
            delay: 40,
            deleteSpeed: Infinity,
            typeSpeed: 40,
          }}
        />
      </div>
    </div>
  );
}

export default Chatbox
