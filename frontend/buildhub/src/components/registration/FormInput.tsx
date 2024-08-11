/**
 * This code was generated by Builder.io.
 */
import React from 'react';

interface FormInputProps {
  label: string;
  placeholder: string;
  type?: string;
}

const FormInput: React.FC<FormInputProps> = ({ label, placeholder, type = 'text' }) => {
  return (
    <div className="flex flex-col w-full max-w-[624px] max-md:max-w-full">
      <label className="leading-snug opacity-[var(--sds-size-stroke-border)] max-md:max-w-full">
        {label}
      </label>
      <div className="flex overflow-hidden items-center px-4 py-3 mt-2 w-full leading-none bg-white rounded-lg border border-solid border-zinc-300 min-w-[240px] max-md:max-w-full">
        <input
          type={type}
          placeholder={placeholder}
          className="flex-1 shrink self-stretch my-auto basis-0 opacity-[var(--sds-size-stroke-border)] max-md:max-w-full"
        />
      </div>
    </div>
  );
};

export default FormInput;