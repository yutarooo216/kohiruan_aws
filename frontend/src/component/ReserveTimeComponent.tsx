import React from 'react';

type ReserveProps = {
  label: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  required?: boolean;
}

export const ReserveTimeComponent = ({ label, value, onChange, required }: ReserveProps) => {
  return (
    <>
      <label>{label}</label><br />
      <select
        value={value}
        onChange={onChange}
        required={required}
      >
        <option value="">時間を選択してください</option>
        <option value="11:00">11:00</option>
        <option value="11:25">11:25</option>
        <option value="11:55">11:55</option>
        <option value="12:20">12:20</option>
        <option value="12:50">12:50</option>
        <option value="13:15">13:15</option>
        <option value="13:45">13:45</option>
        <option value="14:10">14:10</option>
        <option value="14:40">14:40</option>
        <option value="15:05">15:05</option>
        <option value="15:35">15:35</option>
        <option value="16:00">16:00</option>
        <option value="16:30">16:30</option>
        <option value="16:55">16:55</option>
        <option value="17:25">17:25</option>
        <option value="17:50">17:50</option>
        <option value="18:20">18:20</option>
        <option value="18:45">18:45</option>
      </select>
    </>
  );
}