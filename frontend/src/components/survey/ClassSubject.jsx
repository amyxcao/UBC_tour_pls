// import React from 'react';

// export default function ClassSubject({ classSubject, setClassSubject, onNext }) {
//   return (
//     <div className="min-h-screen flex items-center justify-center bg-[#397D7B]">
//       <div className="bg-[#F7F7F0] w-[700px] h-[500px] p-10 rounded-[30px] flex flex-col justify-between items-center shadow-lg">
        
//         {/* Question */}
//         <div className="w-full text-center mt-4">
//           <h1 className="text-2xl font-semibold text-[#2C2C2C]">
//             What is the subject or focus of the class?
//           </h1>
//         </div>

//         {/* Input */}
//         <input
//           type="text"
//           value={classSubject}
//           onChange={(e) => setClassSubject(e.target.value)}
//           placeholder="e.g. History"
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

export default function ClassSubject({ classSubject, setClassSubject, onNext }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#367a79] px-4">
      <div className="survey-wrapper">
        <h1 className="text-2xl font-semibold text-[#2C2C2C] text-center">
          What is the subject or focus of the class?
        </h1>

        <input
          type="text"
          value={classSubject}
          onChange={(e) => setClassSubject(e.target.value)}
          placeholder="e.g. History"
          className="w-full max-w-[400px] h-[60px] text-lg px-6 py-3 bg-[#E1E1E1] rounded-full text-center placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-[#7DB9B6]"
        />

        <button
          onClick={onNext}
          className="mt-6 w-[200px] h-[60px] bg-[#7DB9B6] text-xl font-semibold text-white rounded-full hover:bg-[#6ca7a4] transition"
        >
          Next
        </button>
      </div>
    </div>
  );
}
