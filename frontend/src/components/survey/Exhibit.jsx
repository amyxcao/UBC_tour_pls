// import React from 'react';

// export default function Exhibit({ exhibit, setExhibit, onNext }) {
//   const predefinedExhibit = ['Pictorial Silks', 'Tradition Contemporary', 'Objectifying China'];

//   const handleSelect = (option) => {
//     setExhibit(option === exhibit ? '' : option);
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-[#367a79] px-4">
//       <div className="survey-wrapper">
//         <h1 className="text-2xl font-semibold text-center text-[#2C2C2C] mt-2">
//           Please select an exhibit
//         </h1>

//         <div className="grid grid-cols-3 gap-x-6 gap-y-4 mt-4">
//           {predefinedExhibit.map((option) => (
//             <button
//               key={option}
//               onClick={() => handleSelect(option)}
//               className={`w-[130px] py-3 text-base rounded-full font-medium shadow-sm transition-all duration-200 ${
//                 exhibit === option
//                   ? 'bg-[#7DB9B6] text-white'
//                   : 'bg-[#E1E1E1] text-black hover:bg-[#d4d4d4]'
//               }`}
//             >
//               {option}
//             </button>
//           ))}
//         </div>

//         <button
//           onClick={onNext}
//           className="mt-6 w-[200px] h-[50px] bg-[#7DB9B6] text-xl font-semibold text-white rounded-full hover:bg-[#6ca7a4] transition"
//         >
//           Next
//         </button>
//       </div>
//     </div>
//   );
// }
import React from 'react';

export default function Exhibit({ exhibit, setExhibit, onNext }) {
  const predefinedExhibit = ['Pictorial Silks', 'Tradition Contemporary', 'Objectifying China'];

  const handleSelect = (option) => {
    setExhibit(option === exhibit ? '' : option);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#367a79] px-4">
      <div className="survey-wrapper">
        {/* Header */}
        <h1 className="text-2xl font-semibold text-center text-[#2C2C2C] mt-2 font-sans">
          Please select an exhibit
        </h1>

        {/* Exhibit Buttons */}
        <div className="grid grid-cols-3 gap-x-6 gap-y-4 mt-6">
          {predefinedExhibit.map((option) => (
            <button
              key={option}
              onClick={() => handleSelect(option)}
              className={`w-[180px] py-4 text-lg rounded-full font-sans font-medium shadow-sm transition-all duration-200 ${
                exhibit === option
                  ? 'bg-[#7DB9B6] text-white border-2 border-white'
                  : 'bg-[#E1E1E1] text-black hover:bg-[#d4d4d4] border border-[#C5C5C5]'
              }`}
            >
              {option}
            </button>
          ))}
        </div>

        {/* Next Button */}
        <button
          onClick={onNext}
          className="mt-6 w-[200px] h-[55px] bg-[#7DB9B6] text-xl font-semibold text-white rounded-full hover:bg-[#6ca7a4] transition font-sans"
        >
          Next
        </button>
      </div>
    </div>
  );
}
