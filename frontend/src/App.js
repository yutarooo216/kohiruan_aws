import React, { useState } from 'react';
import { InputField } from './component/InputField.tsx';
import { ReserveTimeComponent } from './component/ReserveTimeComponent.tsx';
import axios from 'axios';

const API_URL = `${process.env.REACT_APP_API_URL}/test/`;

export const App = () => {
  const [reserveDate, setReserveDate] = useState('');
  const [reserveTime, setReserveTime] = useState('');
  const [firstName, setFirstName] = useState('');
  const [firstNameKn, setFirstNameKn] = useState('');
  const [lastName, setLastName] = useState('');
  const [lastNameKn, setLastNameKn] = useState('');
  const [email, setEmail] = useState('');
  const [tel, setTel] = useState('');
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus(null);
    setError(null);

    try {
      await axios.post(API_URL, {
        reserveDate,
        reserveTime,
        firstName,
        firstNameKn,
        lastName,
        lastNameKn,
        email,
        tel,
      });
      setStatus('送信が完了しました。');
    } catch (err) {
      console.error(err);
      setError('送信に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold text-center mb-6">こひる庵予約システム</h1>
      <form onSubmit={handleSubmit}>
        <div className="flex gap-4 mb-4">
          <InputField label="苗字" type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
          <InputField label="名前" type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
        </div>

        <div className="flex gap-4 mb-4">
          <InputField label="苗字（カタカナ）" type="text" value={lastNameKn} onChange={(e) => setLastNameKn(e.target.value)} required />
          <InputField label="名前（カタカナ）" type="text" value={firstNameKn} onChange={(e) => setFirstNameKn(e.target.value)} required />
        </div>

        <div className="flex gap-4 mb-4">
          <InputField label="メールアドレス" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <InputField label="電話番号" type="text" value={tel} onChange={(e) => setTel(e.target.value)} required />
        </div>

        <div className="flex gap-4 mb-4">
          <InputField label="予約日時" type="date" value={reserveDate} onChange={(e) => setReserveDate(e.target.value)} required />
          <ReserveTimeComponent label="予約時間" value={reserveTime} onChange={(e) => setReserveTime(e.target.value)} required />
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-2 px-4 text-white font-bold rounded ${
            loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
          }`}
        >
          {loading ? '送信中...' : '送信'}
        </button>
      </form>

      {status && <p className="text-green-500 mt-4">{status}</p>}
      {error && <p className="text-red-500 mt-4">{error}</p>}
    </div>
  );
};