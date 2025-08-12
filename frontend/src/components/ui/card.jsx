// src/components/ui/card.jsx
import React from "react";

export function Card({ children, className = "" }) {
  return (
    <div className={`rounded-xl border p-6 shadow bg-white ${className}`}>
      {children}
    </div>
  );
}

export function CardContent({ children, className = "" }) {
  return (
    <div className={`text-sm text-gray-700 ${className}`}>
      {children}
    </div>
  );
}
