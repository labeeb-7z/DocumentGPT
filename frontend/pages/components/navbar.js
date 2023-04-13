import React from "react";

const Navbar = () => {
  return (
    <nav class="absolute w-full z-20 top-0 left-0 bg-transparent">
      <div class="flex p-4 justify-between">

        <a href="https://flowbite.com/" class="flex items-left mx-3">
          <span class="self-start text-xl font-semibold whitespace-nowrap">
            ChatDCT
          </span>
        </a>
        <div class="flex md:order-2">
          <div class="relative mr-3 hidden md:block">
            <button className="border text-sm rounded-lg py-2 px-5 font-extrabold border-gray-500">Try Now</button>
          </div>
        </div>
        <div class="hidden md:flex justify-between items-center w-full md:w-auto md:order-1" id="mobile-menu-3">
          <ul class="flex-col md:flex-row flex md:space-x-8 mt-4 md:mt-0 md:text-sm md:font-medium">
            <li>
              <a href="#" class="text-white block pl-3 pr-4 py-0 rounded text-lg" aria-current="page">Home</a>
            </li>
            <li>
              <a href="#" class="text-white block pl-3 pr-4 py-0 rounded text-lg">About</a>
            </li>
            <li>
              <a href="#" class="text-white block pl-3 pr-4 py-0 rounded text-lg">Services</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
