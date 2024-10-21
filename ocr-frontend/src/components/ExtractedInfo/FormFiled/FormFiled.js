import React from 'react';

const FormField = ({ label, value }) => {
    return (
    <div className="flex flex-col mb-4">
      <label className="text-gray-600 font-bold text-left mb-1">{label}:</label>
      <input
        type="text"
        value={value}
        readOnly
        className="p-2 border rounded-lg bg-gray-100 text-gray-700 w-full max-w-lg"
      />
    </div>
  );
};

export default FormField;
