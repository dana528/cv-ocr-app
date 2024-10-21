import React from 'react';
import FormField from './FormFiled/FormFiled';

const CRBookInfo = ({ details }) => {
    console.log(details.CHASSIS_NO);
    console.log(details.FUEL_TYPE);

    return (
    <div className="bg-white shadow-md rounded-lg p-6 max-w-xl mx-auto mt-10">
    <h2 className="text-2xl font-bold mb-6 text-center text-blue-600">Extracted Details</h2>
        <form action=''>
        <FormField label="Registration No" value={details.REGISTRATION_NO} />
        <FormField label="Chassi No" value={details.CHASSIS_NO} />
        <FormField label="Engine No" value={details.ENGINE_NO} />
        <FormField label="Cylinder Capacity" value={details.CYLINDER_CAPACITY} />
        <FormField label="Class of Vehicle" value={details.CLASS_OF_VEHICLE} />
        <FormField label="Taxation Class" value={details.TAXATION_CLASS} />
        <FormField label="Status When Registered" value={details.STATUS_WHEN_REGISTERED}/>
        <FormField label="Fuel Type" value={details.FUEL_TYPE}/>
        </form>
    <div className="space-y-4">
    </div>
    </div>
    );
};

export default CRBookInfo;
