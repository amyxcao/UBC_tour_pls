// import React, { useState } from 'react';

// const categoryOptions = {
//   Dynasty: [
//     "Tang", "Song", "Yuan", "Ming", "Qing"
//   ],
//   Materiality: [
//     "Earthenware", "Porcelain", "Stoneware", "Firing", "Temperature", "Ceramics", "Clay"
//   ],
//   Regions: [
//     "Jizhou", "Jingdezhen", "Longquan", "Yaozhou", "Dehua", "Europe", "Southeast Asia"
//   ],
//   Colours: [
//     "Blue and White", "Monochrome", "Polychrome", "Green", "Brown", "Red", "White", "Yellow", "Celadon", "Wucai"
//   ],
//   Type: [
//     "Court", "Imperial", "Ritual", "Decoration", "Functional", "Curiosities", "Commission"
//   ],
//   Themes: [
//     "Symbolism", "Technique", "Mythical", "Landscapes", "Nature", "Religious", "Import/Export"
//   ]
// };

// export default function TopicDropdowns({ onNext }) {
//   const [selectedOptions, setSelectedOptions] = useState({
//     Dynasty: '',
//     Materiality: '',
//     Regions: '',
//     Colours: '',
//     Type: '',
//     Themes: ''
//   });

//   const [otherInput, setOtherInput] = useState('');
//   const [customTopics, setCustomTopics] = useState([]);

//   const handleChange = (category, value) => {
//     setSelectedOptions((prev) => ({
//       ...prev,
//       [category]: value
//     }));
//   };

//   const handleOtherKeyDown = (e) => {
//     if (e.key === 'Enter' && otherInput.trim() !== '') {
//       e.preventDefault();
//       if (!customTopics.includes(otherInput.trim())) {
//         setCustomTopics([...customTopics, otherInput.trim()]);
//       }
//       setOtherInput('');
//     }
//   };

//   const removeCustomTopic = (topic) => {
//     setCustomTopics((prev) => prev.filter((t) => t !== topic));
//   };

//   const handleSubmit = () => {
//     const cleaned = Object.values(selectedOptions)
//       .filter((val) => typeof val === 'string' && val.trim() !== '')
//       .concat(customTopics);
//     onNext(cleaned);
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-[#397D7B] px-4">
//       <div className="bg-[#F7F7F0] w-full max-w-[720px] p-10 rounded-[30px] flex flex-col items-center shadow-lg space-y-6 overflow-y-auto max-h-[90vh]">

//         <h1 className="text-2xl font-semibold text-center text-[#2C2C2C] leading-snug mb-2">
//           Select relevant topics across the categories below
//         </h1>

//         {/* Dropdown grid */}
//         <div className="grid grid-cols-2 gap-x-6 gap-y-4 w-full">
//           {Object.entries(categoryOptions).map(([category, options]) => (
//             <div key={category} className="flex flex-col">
//               <label className="text-sm font-medium text-gray-700 mb-1">{category}</label>
//               <select
//                 value={selectedOptions[category]}
//                 onChange={(e) => handleChange(category, e.target.value)}
//                 className="h-[45px] px-3 rounded-md border border-gray-300 bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#7DB9B6]"
//               >
//                 <option value="">Select {category}</option>
//                 {options.map((option) => (
//                   <option key={option} value={option}>{option}</option>
//                 ))}
//               </select>
//             </div>
//           ))}
//         </div>

//         {/* Other input with badges */}
//         <div className="w-full flex flex-col mt-2">
//           <label className="text-sm text-gray-600 mb-1">Other:</label>
//           <input
//             type="text"
//             value={otherInput}
//             onChange={(e) => setOtherInput(e.target.value)}
//             onKeyDown={handleOtherKeyDown}
//             placeholder="Press Enter to add multiple custom topics"
//             className="w-full h-[50px] px-4 text-base bg-[#E1E1E1] rounded-full text-center placeholder:text-gray-500 focus:outline-none"
//           />
//           <div className="flex flex-wrap mt-2 gap-2">
//             {customTopics.map((topic, idx) => (
//               <span
//                 key={idx}
//                 className="bg-[#7DB9B6] text-white px-3 py-1 rounded-full text-sm flex items-center space-x-2"
//               >
//                 <span>{topic}</span>
//                 <button
//                   onClick={() => removeCustomTopic(topic)}
//                   className="ml-2 text-white font-bold focus:outline-none"
//                 >
//                   ×
//                 </button>
//               </span>
//             ))}
//           </div>
//         </div>

//         {/* Submit */}
//         <button
//           onClick={handleSubmit}
//           type="button"
//           className="mt-4 w-[200px] h-[50px] bg-[#7DB9B6] text-xl font-semibold text-white rounded-full hover:bg-[#6ca7a4] transition"
//         >
//           Submit
//         </button>
//       </div>
//     </div>
//   );
// }
import React, { useState } from 'react';

const categoryOptions = {
  Dynasty: ['Tang', 'Song', 'Yuan', 'Ming', 'Qing'],
  Materiality: ['Earthenware', 'Porcelain', 'Stoneware', 'Firing', 'Temperature', 'Ceramics', 'Clay'],
  Regions: ['Jizhou', 'Jingdezhen', 'Longquan', 'Yaozhou', 'Dehua', 'Europe', 'Southeast Asia'],
  Colours: ['Blue and White', 'Monochrome', 'Polychrome', 'Green', 'Brown', 'Red', 'White', 'Yellow', 'Celadon', 'Wucai'],
  Type: ['Court', 'Imperial', 'Ritual', 'Decoration', 'Functional', 'Curiosities', 'Commission'],
  Themes: ['Symbolism', 'Technique', 'Mythical', 'Landscapes', 'Nature', 'Religious', 'Import/Export'],
};

export default function TopicDropdowns({ onNext }) {
  const [selectedOptions, setSelectedOptions] = useState({
    Dynasty: '',
    Materiality: '',
    Regions: '',
    Colours: '',
    Type: '',
    Themes: '',
  });

  const [otherInput, setOtherInput] = useState('');
  const [customTopics, setCustomTopics] = useState([]);

  const handleChange = (category, value) => {
    setSelectedOptions((prev) => ({
      ...prev,
      [category]: value,
    }));
  };

  const handleOtherKeyDown = (e) => {
    if (e.key === 'Enter' && otherInput.trim() !== '') {
      e.preventDefault();
      if (!customTopics.includes(otherInput.trim())) {
        setCustomTopics([...customTopics, otherInput.trim()]);
      }
      setOtherInput('');
    }
  };

  const removeCustomTopic = (topic) => {
    setCustomTopics((prev) => prev.filter((t) => t !== topic));
  };

  const handleSubmit = () => {
    const cleaned = Object.values(selectedOptions)
      .filter((val) => typeof val === 'string' && val.trim() !== '')
      .concat(customTopics);
    onNext(cleaned);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#367a79] px-4">
      <div className="survey-wrapper max-w-[720px] space-y-6 overflow-y-auto max-h-[90vh]">
        <h1 className="text-2xl font-semibold text-center text-[#2C2C2C] leading-snug">
          Select relevant topics across the categories below
        </h1>

        <div className="grid grid-cols-2 gap-x-6 gap-y-4 w-full">
          {Object.entries(categoryOptions).map(([category, options]) => (
            <div key={category} className="flex flex-col">
              <label className="text-sm font-medium text-gray-700 mb-1">{category}</label>
              <select
                value={selectedOptions[category]}
                onChange={(e) => handleChange(category, e.target.value)}
                className="h-[45px] px-3 rounded-md border border-gray-300 bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#7DB9B6]"
              >
                <option value="">Select {category}</option>
                {options.map((option) => (
                  <option key={option} value={option}>{option}</option>
                ))}
              </select>
            </div>
          ))}
        </div>

        <div className="w-full flex flex-col mt-2">
          <label className="text-sm text-gray-600 mb-1">Other:</label>
          <input
            type="text"
            value={otherInput}
            onChange={(e) => setOtherInput(e.target.value)}
            onKeyDown={handleOtherKeyDown}
            placeholder="Press Enter to add multiple custom topics"
            className="w-full h-[50px] px-4 text-base bg-[#E1E1E1] rounded-full text-center placeholder:text-gray-500 focus:outline-none"
          />

          <div className="flex flex-wrap mt-2 gap-2">
            {customTopics.map((topic, idx) => (
              <div key={idx} className="custom-topic">
                <span>{topic}</span>
                <button onClick={() => removeCustomTopic(topic)}>×</button>
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={handleSubmit}
          type="button"
          className="w-[200px] h-[50px] bg-[#7DB9B6] text-xl font-semibold text-white rounded-full hover:bg-[#6ca7a4] transition"
        >
          Submit
        </button>
      </div>
    </div>
  );
}
