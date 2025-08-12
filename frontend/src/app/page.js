// 'use client';
// import React, { useState } from 'react';
// import TourGuideInfo from '../components/survey/TourGuideInfo.jsx';
// import TopicDropdowns from '../components/survey/Topics.jsx';
// import Exhibit from '../components/survey/Exhibit.jsx';
// import AgeGroup from '../components/survey/AgeGroup.jsx';
// import ClassSubject from '../components/survey/ClassSubject.jsx';
// import Duration from '../components/survey/Duration.jsx';
// import AdditionalInfo from '../components/survey/AdditionalInfo.jsx';
// import ExhibitSummaryPage from '../components/ExhibitSummaryPage.jsx'; // ✅ NEW IMPORT

// export default function Page() {
//   const [step, setStep] = useState(0);

//   // Survey fields
//   const [guideInfo, setGuideInfo] = useState('');
//   const [exhibit, setExhibit] = useState('');
//   const [ageGroup, setAgeGroup] = useState('');
//   const [classSubject, setClassSubject] = useState('');
//   const [topics, setTopics] = useState([]);
//   const [duration, setDuration] = useState('');
//   const [additionalInfo, setAdditionalInfo] = useState('');

//   // Output
//   const [generatedOutput, setGeneratedOutput] = useState(null);
//   const [loading, setLoading] = useState(false);

//   const steps = [
//     <TourGuideInfo
//       guideInfo={guideInfo}
//       setGuideInfo={setGuideInfo}
//       onNext={() => setStep(step + 1)}
//     />,
//     <Exhibit
//       exhibit={exhibit}
//       setExhibit={setExhibit}
//       onNext={() => setStep(step + 1)}
//     />,
//     <AgeGroup
//       ageGroup={ageGroup}
//       setAgeGroup={setAgeGroup}
//       onNext={() => setStep(step + 1)}
//     />,
//     <ClassSubject
//       classSubject={classSubject}
//       setClassSubject={setClassSubject}
//       onNext={() => setStep(step + 1)}
//     />,
//     <TopicDropdowns
//       onNext={(selected) => {
//         const flattened = Object.values(selected)
//           .flat()
//           .filter((val) => val && val.trim() !== '');
//         setTopics(flattened);
//         setStep(step + 1);
//       }}
//     />,
//     <Duration
//       duration={duration}
//       setDuration={setDuration}
//       onNext={() => setStep(step + 1)}
//     />,
//     <AdditionalInfo
//       additionalInfo={additionalInfo}
//       setAdditionalInfo={setAdditionalInfo}
//       onSubmitSurvey={fetchTour}
//       isLoading={loading}
//     />,
//   ];

//   async function fetchTour() {
//     setLoading(true);

//     try {
//       const res = await fetch('http://localhost:8000/generate', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           major: guideInfo,
//           age_group: ageGroup,
//           class_subject: classSubject,
//           topics_of_interest: topics,
//           exhibit_name: exhibit,
//           tour_length_minutes: parseInt(duration),
//           additional_notes: additionalInfo,
//         }),
//       });

//       const data = await res.json();
//       setGeneratedOutput(data);
//       setStep(step + 1);
//     } catch (err) {
//       console.error('❌ API call failed:', err);
//       alert('Failed to fetch tour. Please try again.');
//     } finally {
//       setLoading(false);
//     }
//   }

//   if (generatedOutput) {
//     return (
//       <ExhibitSummaryPage
//         userInput={{
//           guideInfo,
//           exhibit,
//           ageGroup,
//           classSubject,
//           topics,
//           duration,
//           additionalInfo,
//         }}
//         itinerary={generatedOutput.itinerary}
//         talkingPoints={generatedOutput.talking_points}
//         guideTips={generatedOutput.engagement_tips}
//         onBackClick={() => setStep(steps.length - 1)}
//         onFeedbackClick={() => alert('Thanks for your feedback!')}
//       />
//     );
//   }

//   return steps[step];
// }
'use client';

import React, { useState } from 'react';
import TourGuideInfo from '../components/survey/TourGuideInfo.jsx';
import TopicDropdowns from '../components/survey/Topics.jsx';
import Exhibit from '../components/survey/Exhibit.jsx';
import AgeGroup from '../components/survey/AgeGroup.jsx';
import ClassSubject from '../components/survey/ClassSubject.jsx';
import Duration from '../components/survey/Duration.jsx';
import AdditionalInfo from '../components/survey/AdditionalInfo.jsx';
import ExhibitSummaryPage from '../components/ExhibitSummaryPage.jsx';

export default function Page() {
  const [step, setStep] = useState(0);

  // Survey fields
  const [guideInfo, setGuideInfo] = useState('');
  const [exhibit, setExhibit] = useState('');
  const [ageGroup, setAgeGroup] = useState('');
  const [classSubject, setClassSubject] = useState('');
  const [topics, setTopics] = useState([]);
  const [duration, setDuration] = useState('');
  const [additionalInfo, setAdditionalInfo] = useState('');

  // Output
  const [generatedOutput, setGeneratedOutput] = useState(null);
  const [loading, setLoading] = useState(false);

  const steps = [
    <TourGuideInfo guideInfo={guideInfo} setGuideInfo={setGuideInfo} onNext={() => setStep(step + 1)} />,
    <Exhibit exhibit={exhibit} setExhibit={setExhibit} onNext={() => setStep(step + 1)} />,
    <AgeGroup ageGroup={ageGroup} setAgeGroup={setAgeGroup} onNext={() => setStep(step + 1)} />,
    <ClassSubject classSubject={classSubject} setClassSubject={setClassSubject} onNext={() => setStep(step + 1)} />,
    <TopicDropdowns
      onNext={(selected) => {
        const flattened = Object.values(selected).flat();
        setTopics(flattened);
        setStep(step + 1);
      }}
    />,
    <Duration duration={duration} setDuration={setDuration} onNext={() => setStep(step + 1)} />,
    <AdditionalInfo
      additionalInfo={additionalInfo}
      setAdditionalInfo={setAdditionalInfo}
      onSubmitSurvey={fetchTour}
      isLoading={loading}
    />,
  ];

  async function fetchTour() {
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          major: guideInfo,
          age_group: ageGroup,
          class_subject: classSubject,
          topics_of_interest: topics,
          exhibit_name: exhibit,
          tour_length_minutes: parseInt(duration),
          additional_notes: additionalInfo,
        }),
      });

      const data = await res.json();
      setGeneratedOutput(data);
      setStep(step + 1);
    } catch (err) {
      console.error('❌ API call failed:', err);
      alert('Failed to fetch tour. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  if (generatedOutput) {
    return (
      <ExhibitSummaryPage
        itinerary={generatedOutput.itinerary}
        talkingPoints={generatedOutput.talking_points}
        engagementTips={generatedOutput.engagement_tips}
      />
    );
  }

  return steps[step];
}
