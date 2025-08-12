// import React from 'react';

// export default function TourGuideInfo({ guideInfo, setGuideInfo, onNext }) {
//   return (
//     <div className="min-h-screen flex items-center justify-center bg-[#397D7B]">
//       <div className="bg-[#F7F7F0] w-[700px] h-[500px] p-10 rounded-[30px] flex flex-col justify-between items-center shadow-lg">
        
//         {/* Question */}
//         <div className="w-full text-center mt-4">
//           <h1 className="text-2xl font-semibold text-[#2C2C2C]">
//             What is your background?
//           </h1>
//         </div>

//         {/* Input */}
//         <input
//           type="text"
//           value={guideInfo}
//           onChange={(e) => setGuideInfo(e.target.value)}
//           placeholder="e.g. Art History"
//           className="w-[400px] h-[60px] text-lg px-6 py-3 bg-[#E1E1E1] rounded-full text-center placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-[#7DB9B6]"
//         />

//         {/* Next Button */}
//         <button
//           onClick={onNext}
//           className="w-[200px] h-[60px] bg-[#7DB9B6] text-xl font-semibold text-white rounded-full hover:bg-[#6ca7a4] transition"
//         >
//           Next
//         </button>

      
//       </div>
//     </div>
//   );
// }
import React from 'react';

export default function TourGuideInfo({ guideInfo, setGuideInfo, onNext }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#367a79] px-4">
      <div className="survey-wrapper">
        {/* Question */}
        <div className="w-full text-center mb-6">
          <h1 className="text-2xl font-semibold text-[#2C2C2C]">
            What is your background?
          </h1>
        </div>

        {/* Input */}
        <input
          type="text"
          value={guideInfo}
          onChange={(e) => setGuideInfo(e.target.value)}
          placeholder="e.g. Art History"
          className="w-full max-w-[500px] h-[75px] text-2xl px-6 bg-[#E1E1E1] text-center placeholder:text-gray-500 
            rounded-full border border-[#C5C5C5] shadow-inner 
            focus:outline-none focus:ring-2 focus:ring-[#7DB9B6] transition"
        />

        {/* Next Button */}
        <button
          onClick={onNext}
          className="mt-6 w-[240px] h-[70px] bg-[#7DB9B6] text-xl font-semibold text-white rounded-full 
            shadow-lg hover:bg-[#6ca7a4] transition-all duration-200"
        >
          Next
        </button>
      </div>
    </div>
  );
}



