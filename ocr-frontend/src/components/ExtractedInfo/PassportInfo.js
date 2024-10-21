import React from 'react';
import FormField from './FormFiled/FormFiled';

const PassportInfo = ({ details }) => {
    console.log(details.mrz_data.names);
    return (
    <div className="bg-white shadow-md rounded-lg p-6 max-w-xl mx-auto mt-10">
    <h2 className="text-2xl font-bold mb-6 text-center text-blue-600">Extracted Details</h2>
        <form action=''>
        <FormField label="Name" value={details.mrz_data.names} />
        <FormField label="Surname" value={details.mrz_data.surname} />
        <FormField label="Country Code" value={details.mrz_data.country_code} />
        <FormField label="Country" value={details.mrz_data.country} />
        <FormField label="NIC No" value={details.mrz_data.nic_number} />
        <FormField label="Date of Birth" value={details.mrz_data.date_of_birth} />
        <FormField label="Date of Issue" value={details.mrz_data.issue_date}/>
        <FormField label="Date of Expiry" value={details.mrz_data.expiration_date}/>
        <FormField label="Sex" value={details.mrz_data.sex}/>
        <FormField label="Type" value={details.mrz_data.type}/>
        <FormField label="MRZ Code" value={details.mrz_data.mrz_code}/>
        </form>
    <div className="space-y-4">
    </div>
    </div>
    );
};

export default PassportInfo;
