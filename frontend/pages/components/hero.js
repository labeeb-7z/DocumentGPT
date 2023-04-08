import React, { useRef, useEffect, useState, useCallback } from 'react';
import { gsap } from 'gsap';
import { MotionPathPlugin } from 'gsap/dist/MotionPathPlugin';
import Snowfall from 'react-snowfall'
import Typewriter from 'typewriter-effect';
import UploadPdf from './uploadpdf';

gsap.registerPlugin(MotionPathPlugin);

const Hero = () => {

  const show = useRef(null);
  const logo = useRef(null);
  const logo2 = useRef(null);
  const logo3 = useRef(null);
  const path = useRef(null);
  const div = useRef(null);

  const handleScrollClick = (item) => {
    show.current.scrollIntoView({
      behavior: 'smooth'
    });
  };

  const [center, setcenter] = useState(false)
  const [center2, setcenter2] = useState(false)
  const [center3, setcenter3] = useState(false)



  useEffect(() => {
    const el = logo.current
    const el2 = logo2.current
    const el3 = logo3.current
    const el4 = path.current
    const el5 = div.current

    gsap.set(el4, { x: -30, y: -30 });
    gsap.to(el,
      {
        duration: 1,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.665,
          end: 0.665,
        }
      });

    gsap.to(el2,
      {
        duration: 2,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.5,
          end: 0.5,
        },
      });

    gsap.to(el3,
      {
        duration: 2,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.33,
          end: 0.33,
        },
      });
  }, [])



  const logoClicked = (event) => {
    const el = logo.current
    const el2 = logo2.current
    const el3 = logo3.current
    const el4 = path.current

    gsap.to(el,
      {
        duration: 1,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.665,
          end: 0.5,
        },
      });

    gsap.to(el2,
      {
        duration: 1,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.5,
          end: 0.33,
        },
      });

    gsap.to(el3,
      {
        duration: 1,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.33,
          end: -0.33,
        },
      });



    setcenter(true);
    setcenter2(false);
    setcenter3(false);
    handleScrollClick(logo);
  }

  const logoClicked2 = (event) => {
    const el = logo.current
    const el2 = logo2.current
    const el3 = logo3.current
    const el4 = path.current

    gsap.to(el,
      {
        duration: 1,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.5,
          end: 0.665,
        },
      });

    gsap.to(el2,
      {
        duration: 1,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.33,
          end: 0.5,
        },
      });

    gsap.to(el3,
      {
        duration: 1,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.665,
          end: 1.33
        },
      });


    setcenter(false)
    setcenter2(true)
    setcenter3(false)
    handleScrollClick(logo2);
  }

  const logoClicked3 = (event) => {
    const el = logo.current
    const el2 = logo2.current
    const el3 = logo3.current
    const el4 = path.current

    gsap.to(el,
      {
        duration: 1,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.665,
          end: 1.33,
        },
      });

    gsap.to(el2,
      {
        duration: 1,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.5,
          end: 0.665,
        },
      });

    gsap.to(el3,
      {
        duration: 1,
        ease: 'none',
        motionPath: {
          path: el4,
          align: el4,
          start: 0.33,
          end: 0.5
        },
      });


    setcenter(false)
    setcenter2(false)
    setcenter3(true)
    handleScrollClick(logo3);
  }

  return (
    <div ref={div} className='w-[98.9vw] h-[70rem] text-white scroll-smooth bg-[#121416]'>
      <Snowfall
        snowflakeCount={20}
        wind={[0, 0]}
        speed={[0, 0.5]}
        radius={[3, 3]}
      />
      <svg className='mt-[-15rem] absolute h-[80rem] w-[80rem] left-[50%] translate-x-[-49.5%] border-2 rounded-full border-gray-500 shadow-3xl' viewBox="0 0 1267 1267" shape-rendering="geometricPrecision" text-rendering="geometricPrecision">
        <path ref={path} d="M 633.5,0
           a 633.5,633.5 0 0 1 0,1267
           a 633.5,633.5 0 0 1 0,-1267"
          fill="none" stroke="#fff" stroke-width="0" />
      </svg>
      <div className='h-[65rem] w-[80rem] mx-auto px-10 py-10 text-center'>
        <div>
          <h1 className='text-6xl mt-32'><span class="text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400 font-extrabold">DocumentGPT</span></h1> <h1 className='text-md tracking-widest my-8 font-semibold'>Helps</h1>
          <h1 className='text-5xl font-bold'>
            <Typewriter
              options={{
                strings: [
                  "Summarizing",
                  "Generating Q&As",
                  "Expedite Learning of",
                  "Research Papers, Articles & Books"
                ],
                autoStart: true,
                loop: true,
                delay: 40,
                deleteSpeed: 40,
                typeSpeed: 40,
              }}
            />
          </h1>
        </div>
      </div>
      <svg
        ref={logo}
        xmlns="http://www.w3.org/2000/svg"
        fill="none" viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        className='border-2 border-red-500 h-[7rem] p-5 rounded-full bg-black absolute'
        onClick={!center ? logoClicked : null}
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
      </svg>

      <svg
        ref={logo2}
        viewBox="0 0 24 24"
        fill="currentColor"
        className='border-2 border-green-500 h-[7rem] p-5 rounded-full bg-black absolute'
        onClick={!center2 ? logoClicked2 : null}
      >
        <path d="M18 15H6l-4 4V3a1 1 0 011-1h15a1 1 0 011 1v11a1 1 0 01-1 1m5-6v14l-4-4H8a1 1 0 01-1-1v-1h14V8h1a1 1 0 011 1M8.19 4c-.87 0-1.57.2-2.11.59-.52.41-.78.98-.77 1.77l.01.03h1.93c.01-.3.1-.53.28-.69a1 1 0 01.66-.23c.31 0 .57.1.75.28.18.19.26.45.26.75 0 .32-.07.59-.23.82-.14.23-.35.43-.61.59-.51.34-.86.64-1.05.91C7.11 9.08 7 9.5 7 10h2c0-.31.04-.56.13-.74.09-.18.26-.36.51-.52.45-.24.82-.53 1.11-.93.29-.4.44-.81.44-1.31 0-.76-.27-1.37-.81-1.82C9.85 4.23 9.12 4 8.19 4M7 11v2h2v-2H7m6 2h2v-2h-2v2m0-9v6h2V4h-2z" />
      </svg>
      <svg
        ref={logo3}
        xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor"
        className='border-2 border-blue-500 h-[7rem] p-5 rounded-full bg-black absolute'
        onClick={!center3 ? logoClicked3 : null}
      >
        <path strokeLinecap="round" strokeLinejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342M6.75 15a.75.75 0 100-1.5.75.75 0 000 1.5zm0 0v-3.675A55.378 55.378 0 0112 8.443m-7.007 11.55A5.981 5.981 0 006.75 15.75v-1.5" />
      </svg>
      <div ref={show} className='ml-10 w-full opacity-0'></div>
      <div className='absolute top-[30rem] left-[50%] -translate-x-[50%]'>
        <UploadPdf />
      </div>
    </div>
  )
}

export default Hero