// src/components/ui/button.jsx

import React from "react";

export function Button({ children, className = "", ...props }) {
  return (
    <button
      className={`inline-flex items-center justify-center rounded-md bg-teal-600 px-6 py-2 text-sm font-medium text-white shadow-sm hover:bg-teal-700 transition-colors ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
