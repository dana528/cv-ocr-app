// src/components/Tabs/Tabs.js
import React from 'react';
import { FaIdCard, FaPassport, FaCar } from 'react-icons/fa';

const Tabs = ({ activeTab, setActiveTab }) => {
  return (
    <div className="flex justify-evenly mb-5">
  <ul className="flex flex-wrap text-sm font-medium text-center text-gray-500 dark:text-gray-400">
    <li className="me-2">
      <a
        href="#"
        className={`inline-block px-4 py-3 rounded-lg ${
          activeTab === 'dl' ? 'text-white bg-blue-600' : 'hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 dark:hover:text-white'
        }`}
        onClick={() => setActiveTab('dl')}
      >
        <FaIdCard className="inline-block mr-2" />
        Driving License Information
      </a>
    </li>
    <li className="me-2">
      <a
        href="#"
        className={`inline-block px-4 py-3 rounded-lg ${
          activeTab === 'passport' ? 'text-white bg-blue-600' : 'hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 dark:hover:text-white'
        }`}
        onClick={() => setActiveTab('passport')}
      >
        <FaPassport className="inline-block mr-2" />
        Passport Information
      </a>
    </li>
    <li className="me-2">
      <a
        href="#"
        className={`inline-block px-4 py-3 rounded-lg ${
          activeTab === 'crbook' ? 'text-white bg-blue-600' : 'hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 dark:hover:text-white'
        }`}
        onClick={() => setActiveTab('crbook')}
      >
        <FaCar className="inline-block mr-2" />
        Vehicle CR Book Information
      </a>
    </li>
  </ul>
</div>

  );
};

export default Tabs;
