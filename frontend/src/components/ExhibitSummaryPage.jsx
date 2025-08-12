"use client";

import React, { useRef } from "react";

export default function ExhibitSummaryPage({ itinerary, talkingPoints, engagementTips }) {
  const contentRef = useRef();

  const handleExport = async () => {
    const html2pdf = (await import("html2pdf.js")).default;

    const element = contentRef.current;
    const opt = {
      margin: 0.5,
      filename: "Custom-Tour-Plan.pdf",
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
    };

    html2pdf().set(opt).from(element).save();
  };

  return (
    <div className="exhibit-summary min-h-screen bg-[#F1FAF9] py-8 px-4 flex items-center justify-center border-[70px] border-[#397D7B]">
      <div
        ref={contentRef}
        className="w-full max-w-4xl bg-[#397D7B] rounded-3xl shadow-xl px-6 py-10 md:px-10 md:py-12 space-y-10 text-left"
      >
        {/* Title */}
        <h1 className="text-3xl font-bold text-center text-white">Your Custom Tour Plan</h1>

        {/* Itinerary Section */}
        <section>
          <h2 className="text-2xl font-semibold mb-4 text-white">🗺️ Itinerary</h2>
          <ul className="space-y-6">
            {Array.isArray(itinerary?.itinerary) &&
              itinerary.itinerary.map((item, index) => (
                <li
                  key={index}
                  className="flex justify-between items-start border-b border-gray-300 pb-4 gap-x-10 text-white"
                >
                  <span className="text-sm font-mono">{item.time}</span>
                  <span className="text-base font-medium">{item.activity}</span>
                </li>
              ))}
          </ul>
        </section>

        {/* Talking Points Section */}
        <section>
          <h2 className="text-2xl font-semibold mb-4 text-white">💬 Key Talking Points</h2>
          <div className="space-y-6 text-white">
            {Array.isArray(talkingPoints?.themes) &&
              talkingPoints.themes.map((theme, idx) => (
                <div key={idx}>
                  <h3 className="text-lg font-semibold mb-1">{theme.title}</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {theme.points.map((point, i) => (
                      <li key={i}>{point}</li>
                    ))}
                  </ul>
                </div>
              ))}
          </div>
        </section>

        {/* Engagement Tips Section */}
        <section>
          <h2 className="text-2xl font-semibold mb-4 text-white">🎲 Engagement Tips</h2>
          <div className="space-y-6 text-white">
            {engagementTips?.tone_framing?.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-1">Tone & Framing</h3>
                <ul className="list-disc list-inside">
                  {engagementTips.tone_framing.map((tip, i) => (
                    <li key={i}>{tip}</li>
                  ))}
                </ul>
              </div>
            )}
            {engagementTips?.key_takeaways?.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-1">Key Takeaways</h3>
                <ul className="list-disc list-inside">
                  {engagementTips.key_takeaways.map((tip, i) => (
                    <li key={i}>{tip}</li>
                  ))}
                </ul>
              </div>
            )}
            {engagementTips?.creative_activities?.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-1">Creative Activities</h3>
                <ul className="list-disc list-inside">
                  {engagementTips.creative_activities.map((tip, i) => (
                    <li key={i}>{tip}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </section>

        {/* Export to PDF Button */}
        <div className="flex justify-center pt-4">
         <button
  onClick={handleExport}
  className="no-print px-6 py-3 bg-white text-[#397D7B] font-semibold rounded-full hover:bg-gray-100 transition"
>
  Export to PDF
</button>
        </div>
      </div>
    </div>
  );
}
