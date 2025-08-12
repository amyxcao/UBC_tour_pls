// import React, { useState } from 'react';

// export default function AdditionalInfo({
//   additionalInfo,
//   setAdditionalInfo,
//   onSubmitSurvey,
//   isLoading,
// }) {
//   const [error, setError] = useState('');

//   const handleSubmit = () => {
//     if (!additionalInfo.trim()) {
//       setError('Please fill out this field or write "N/A".');
//       return;
//     }
//     setError('');
//     onSubmitSurvey(); // triggers fetchTour from page.js
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-[#397D7B]">
//       <div className="bg-[#F7F7F0] w-[700px] h-[500px] p-10 rounded-[30px] flex flex-col justify-between items-center shadow-lg">
//         {/* Question */}
//         <div className="w-full text-center mt-4">
//           <h1 className="text-2xl font-semibold text-[#2C2C2C]">
//             Anything else we should know about the group?
//           </h1>
//         </div>

//         {/* Input */}
//         <input
//           type="text"
//           value={additionalInfo}
//           onChange={(e) => setAdditionalInfo(e.target.value)}
//           placeholder="Text Input..."
//           className="w-[400px] h-[60px] text-lg px-6 py-3 bg-[#E1E1E1] rounded-full text-center placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-[#7DB9B6]"
//         />
//         {error && <p className="text-red-500 text-sm mt-2">{error}</p>}

//         {/* Submit Button */}
//         <button
//           onClick={handleSubmit}
//           disabled={isLoading}
//           className={`w-[200px] h-[60px] text-xl font-semibold rounded-full transition ${
//             isLoading
//               ? 'bg-gray-400 text-white cursor-not-allowed'
//               : 'bg-[#7DB9B6] text-white hover:bg-[#6ca7a4]'
//           }`}
//         >
//           {isLoading ? 'Generating...' : 'Submit'}
//         </button>
//       </div>
//     </div>
//   );
// }
import React, { useState } from 'react';

export default function AdditionalInfo({
  additionalInfo,
  setAdditionalInfo,
  onSubmitSurvey,
  isLoading,
}) {
  const [error, setError] = useState('');

  const handleSubmit = () => {
    if (!additionalInfo.trim()) {
      setError('Please fill out this field or write "N/A".');
      return;
    }
    setError('');
    onSubmitSurvey();
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#367a79] px-4">
      <div className="survey-wrapper">
        <h1 className="text-2xl font-semibold text-[#2C2C2C] text-center">
          Anything else we should know about the group?
        </h1>

        <input
          type="text"
          value={additionalInfo}
          onChange={(e) => setAdditionalInfo(e.target.value)}
          placeholder="Text Input..."
          className="w-full max-w-[400px] h-[60px] text-lg px-6 py-3 bg-[#E1E1E1] rounded-full text-center placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-[#7DB9B6]"
        />
        {error && <p className="text-red-500 text-sm mt-2">{error}</p>}

        <button
          onClick={handleSubmit}
          disabled={isLoading}
          className={`mt-6 w-[200px] h-[60px] text-xl font-semibold rounded-full transition ${
            isLoading
              ? 'bg-gray-400 text-white cursor-not-allowed'
              : 'bg-[#7DB9B6] text-white hover:bg-[#6ca7a4]'
          }`}
        >
          {isLoading ? 'Generating...' : 'Submit'}
        </button>
      </div>
    </div>
  );
}
