// // import React from 'react';

// // export default function Duration({ duration, setDuration, onNext }) {
// //   const predefinedDuration = ['30 min', '45 min', '1 hour'];

// //   const handleSelect = (option) => {
// //     setDuration(option === duration ? '' : option); // toggle selection
// //   };

// //   return (
// //     <div className="min-h-screen flex items-center justify-center bg-[#397D7B]">
// //       <div className="bg-[#F7F7F0] w-[700px] h-[550px] p-10 rounded-[30px] flex flex-col justify-between items-center shadow-lg">
        
// //         {/* Question */}
// //         <h1 className="text-2xl font-semibold text-center text-[#2C2C2C] mt-6">
// //           Select desired tour duration
// //         </h1>

// //         {/* Tag Grid */}
// //         <div className="grid grid-cols-3 gap-x-6 gap-y-4 mt-4">
// //           {predefinedDuration.map((option) => (
// //             <button
// //               key={option}
// //               onClick={() => handleSelect(option)}
// //               className={`w-[130px] py-3 text-base rounded-full font-medium shadow-sm transition-all duration-200 ${
// //                 duration === option
// //                   ? 'bg-[#7DB9B6] text-white'
// //                   : 'bg-[#E1E1E1] text-black hover:bg-[#d4d4d4]'
// //               }`}
// //             >
// //               {option}
// //             </button>
// //           ))}
// //         </div>

// //         {/* Next Button */}
// //         <button
// //           onClick={onNext}
// //           className="mt-4 w-[200px] h-[50px] bg-[#7DB9B6] text-xl font-semibold text-white rounded-full hover:bg-[#6ca7a4] transition"
// //         >
// //           Next
// //         </button>

     
// //       </div>
// //     </div>
// //   );
// // }
// import React from 'react';

// export default function Duration({ duration, setDuration, onNext }) {
//   const options = [
//     { label: '30 min', value: 30 },
//     { label: '45 min', value: 45 },
//     { label: '1 hour', value: 60 }
//   ];

//   const handleSelect = (value) => {
//     setDuration(duration === value ? '' : value); // store numeric value in minutes
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-[#397D7B]">
//       <div className="bg-[#F7F7F0] w-[700px] h-[550px] p-10 rounded-[30px] flex flex-col justify-between items-center shadow-lg">
        
//         {/* Question */}
//         <h1 className="text-2xl font-semibold text-center text-[#2C2C2C] mt-6">
//           Select desired tour duration
//         </h1>

//         {/* Tag Grid */}
//         <div className="grid grid-cols-3 gap-x-6 gap-y-4 mt-4">
//           {options.map(({ label, value }) => (
//             <button
//               key={label}
//               onClick={() => handleSelect(value)}
//               className={`w-[130px] py-3 text-base rounded-full font-medium shadow-sm transition-all duration-200 ${
//                 duration === value
//                   ? 'bg-[#7DB9B6] text-white'
//                   : 'bg-[#E1E1E1] text-black hover:bg-[#d4d4d4]'
//               }`}
//             >
//               {label}
//             </button>
//           ))}
//         </div>

//         {/* Next Button */}
//         <button
//           onClick={onNext}
//           className="mt-4 w-[200px] h-[50px] bg-[#7DB9B6] text-xl font-semibold text-white rounded-full hover:bg-[#6ca7a4] transition"
//         >
//           Next
//         </button>
//       </div>
//     </div>
//   );
// }
import React from 'react';

export default function Duration({ duration, setDuration, onNext }) {
  const options = [
    { label: '30 min', value: 30 },
    { label: '45 min', value: 45 },
    { label: '1 hour', value: 60 }
  ];

  const handleSelect = (value) => {
    setDuration(duration === value ? '' : value);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#367a79] px-4">
      <div className="survey-wrapper">
        <h1 className="text-2xl font-semibold text-center text-[#2C2C2C] mt-2">
          Select desired tour duration
        </h1>

        <div className="grid grid-cols-3 gap-x-6 gap-y-4 mt-4">
          {options.map(({ label, value }) => (
            <button
              key={label}
              onClick={() => handleSelect(value)}
              className={`w-[130px] py-3 text-base rounded-full font-medium shadow-sm transition-all duration-200 ${
                duration === value
                  ? 'bg-[#7DB9B6] text-white'
                  : 'bg-[#E1E1E1] text-black hover:bg-[#d4d4d4]'
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        <button
          onClick={onNext}
          className="mt-6 w-[200px] h-[50px] bg-[#7DB9B6] text-xl font-semibold text-white rounded-full hover:bg-[#6ca7a4] transition"
        >
          Next
        </button>
      </div>
    </div>
  );
}
