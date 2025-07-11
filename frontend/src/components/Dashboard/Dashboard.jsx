import { useEffect } from 'react'
import axios from 'axios'
import axiosInstance from '../../axiosinstance'

const Dashboard = () => {
    useEffect(() => {
        const fetchProtectedData = async () => {
            try {
                const response = await axiosInstance.get('/protected-view/');
            } catch(error) {
                console.error('Error fetching data: ', error);
            }
        }
        fetchProtectedData();
    }, [])
  return (
    <div className='text-light'>Dashboard</div>
  )
}

export default Dashboard;