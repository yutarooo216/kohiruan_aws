import React from 'react';

type InputProps = {
    label: string;
    type: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    required?: boolean;
}

// inputfieldの定義
export const InputField = ({ label, type, value, onChange, required }) => {
    return (
      <div className="flex flex-col">
        <label className="mb-1 text-sm font-medium text-gray-700">{label}</label>
        <input
          type={type}
          value={value}
          onChange={onChange}
          required={required}
          className="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    );
  };