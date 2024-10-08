/**
 * This code was generated by Builder.io.
 */
import React from 'react';
import BusinessRegistrationForm from './BusinessRegistrationForm';

const RegisterBusinessPage: React.FC = () => {
  const handleSubmit = (businessName: string) => {
    console.log('Business name submitted:', businessName);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="max-w-md w-full">
        <h1 className="text-3xl font-bold text-center mb-6">Register Your Business</h1>
        <BusinessRegistrationForm onSubmit={handleSubmit} />
      </div>
    </div>
  );
};

export default RegisterBusinessPage;