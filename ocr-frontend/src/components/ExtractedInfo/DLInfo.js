import React from 'react';
import FormField from './FormFiled/FormFiled';

const DLInfo = ({ details }) => {
    console.log(details);
    console.log(details.Name);
    console.log(details.Address);
    console.log(details.National_Identification_Card_No);
    return (
    <div className="bg-white shadow-md rounded-lg p-6 max-w-xl mx-auto mt-10">
        <h2 className="text-2xl font-bold mb-6 text-center text-blue-600">Extracted Details</h2>
            <form action=''>
            <FormField label="Name" value={details.Name} />
            <FormField label="NIC" value={details.National_Identification_Card_No} />
            <FormField label="Driving License No" value={details.Driving_Licence_No} />
            <FormField label="Address" value={details.Address} />
            <FormField label="Date of Birth" value={details.Data_Of_Birth} />
            <FormField label="Date of Issue" value={details.Date_Of_Issue} />
            <FormField label="Date of Expiry" value={details.Date_Of_Expiry}/>
            <FormField label="Blood Group"value={details.Blood_Group}/>
            </form>
    <div className="space-y-4">
    </div>
    </div>
    );
};

export default DLInfo;
