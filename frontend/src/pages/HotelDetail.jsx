import React, { useEffect, useState, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getHotel, createReservation, getRoomAvailability } from '../services/api';
import { AuthContext } from '../context/AuthContext';

const RoomAvailability = ({ roomId }) => {
    const [availability, setAvailability] = useState([]);
    const [loading, setLoading] = useState(false);
    const [showCalendar, setShowCalendar] = useState(false);
    const [currentDate, setCurrentDate] = useState(new Date());

    const fetchAvailability = async () => {
        setLoading(true);
        try {
            const res = await getRoomAvailability(roomId);
            console.log("Availability for room", roomId, res.data); // Debug log
            setAvailability(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const toggleCalendar = () => {
        if (!showCalendar) {
            fetchAvailability();
        }
        setShowCalendar(!showCalendar);
    };

    const isDateBooked = (dateStr) => {
        return availability.some(range => {
            return dateStr >= range.check_in && dateStr < range.check_out;
        });
    };

    const renderCalendar = () => {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const firstDayOfMonth = new Date(year, month, 1).getDay();

        const days = [];
        for (let i = 0; i < firstDayOfMonth; i++) {
            days.push(<div key={`empty-${i}`} style={{ padding: '10px' }}></div>);
        }

        for (let d = 1; d <= daysInMonth; d++) {
            // Construct YYYY-MM-DD string manually to avoid timezone issues
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;

            const booked = isDateBooked(dateStr);

            // Check if today
            const today = new Date();
            const isToday = dateStr === `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

            days.push(
                <div key={d} style={{
                    padding: '8px',
                    textAlign: 'center',
                    background: booked ? '#fee2e2' : (isToday ? '#e0e7ff' : '#f0fdf4'),
                    color: booked ? '#dc2626' : (isToday ? '#4f46e5' : '#166534'),
                    borderRadius: '4px',
                    fontSize: '0.9rem',
                    fontWeight: 'bold',
                    border: '1px solid ' + (booked ? '#fecaca' : '#bbf7d0'),
                    cursor: booked ? 'not-allowed' : 'pointer'
                }} title={booked ? 'Booked' : 'Available'}>
                    {d}
                </div>
            );
        }

        return (
            <div style={{ marginTop: '1rem', background: 'white', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                <div style={{ textAlign: 'center', fontWeight: 'bold', marginBottom: '1rem' }}>
                    {currentDate.toLocaleString('default', { month: 'long', year: 'numeric' })}
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: '5px' }}>
                    {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((d, i) => (
                        <div key={i} style={{ textAlign: 'center', fontSize: '0.8rem', color: '#666', fontWeight: 'bold' }}>{d}</div>
                    ))}
                    {days}
                </div>
                <div style={{ display: 'flex', gap: '10px', marginTop: '10px', fontSize: '0.8rem', justifyContent: 'center' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><div style={{ width: 10, height: 10, background: '#fee2e2', border: '1px solid #fecaca' }}></div> Booked</span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><div style={{ width: 10, height: 10, background: '#f0fdf4', border: '1px solid #bbf7d0' }}></div> Available</span>
                </div>
            </div>
        );
    };

    return (
        <div style={{ marginTop: '1rem' }}>
            <button
                type="button" // Prevent form submit
                onClick={toggleCalendar}
                style={{
                    background: 'none',
                    border: 'none',
                    color: 'var(--primary-color)',
                    cursor: 'pointer',
                    fontWeight: '600',
                    fontSize: '0.9rem',
                    padding: 0
                }}
            >
                {showCalendar ? 'Hide Availability Calendar' : '📅 Check Availability'}
            </button>
            {showCalendar && (loading ? <div style={{ marginTop: '0.5rem' }}>Loading...</div> : renderCalendar())}
        </div>
    );
};

export default function HotelDetail() {
    const { id } = useParams();
    const [hotel, setHotel] = useState(null);
    const [loading, setLoading] = useState(true);
    const { user } = useContext(AuthContext);
    const navigate = useNavigate();

    const [bookingData, setBookingData] = useState({
        room: null,
        check_in: '',
        check_out: ''
    });

    useEffect(() => {
        getHotel(id).then(res => {
            setHotel(res.data);
            setLoading(false);
        });
    }, [id]);

    const handleBook = async (e) => {
        e.preventDefault();
        if (!user) {
            alert('Please login to book a room');
            navigate('/login');
            return;
        }
        try {
            await createReservation({
                room: bookingData.room,
                check_in: bookingData.check_in,
                check_out: bookingData.check_out
            });
            alert('Reservation successful!');
            navigate('/profile');
        } catch (err) {
            alert(err.response?.data?.non_field_errors || err.response?.data?.detail || 'Booking failed');
        }
    };

    if (loading) return <div className="container" style={{ textAlign: 'center', marginTop: '4rem' }}>Loading...</div>;

    return (
        <div className="container">
            <div className="detail-header">
                <img src={hotel.image || 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3'} alt={hotel.name} className="detail-img" />
                <div className="detail-content">
                    <h1>{hotel.name}</h1>
                    <div className="rating">★ {hotel.rating} Excellent</div>
                    <p style={{ marginBottom: '1rem', color: 'var(--text-secondary)' }}>📍 {hotel.address}</p>
                    <p style={{ lineHeight: '1.8' }}>{hotel.description}</p>
                </div>
            </div>

            <h3 style={{ fontSize: '1.8rem', marginBottom: '1.5rem' }}>Available Rooms</h3>
            <div className="hotel-grid">
                {hotel.rooms.map(room => (
                    <div key={room.id} className="room-card">
                        <div style={{ padding: '1.5rem', background: 'var(--bg-color)', borderBottom: '1px solid var(--border-color)' }}>
                            <h4 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{room.room_type} Room</h4>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <span style={{ fontWeight: '700', color: 'var(--primary-color)', fontSize: '1.2rem' }}>${room.price_per_night} <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: 'normal' }}>/ night</span></span>
                                <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>👥 {room.capacity} Guests</span>
                            </div>
                            <RoomAvailability roomId={room.id} />
                        </div>

                        <div style={{ padding: '1.5rem' }}>
                            <form onSubmit={handleBook} className="booking-form">
                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                                    <div>
                                        <label style={{ fontSize: '0.85rem', fontWeight: '600', display: 'block', marginBottom: '5px' }}>Check-in</label>
                                        <input
                                            type="date"
                                            required
                                            min={new Date().toISOString().split('T')[0]}
                                            style={{ width: '100%', margin: 0 }}
                                            onChange={e => setBookingData({ ...bookingData, check_in: e.target.value, room: room.id })}
                                        />
                                    </div>
                                    <div>
                                        <label style={{ fontSize: '0.85rem', fontWeight: '600', display: 'block', marginBottom: '5px' }}>Check-out</label>
                                        <input
                                            type="date"
                                            required
                                            min={bookingData.check_in || new Date().toISOString().split('T')[0]}
                                            style={{ width: '100%', margin: 0 }}
                                            onChange={e => setBookingData({ ...bookingData, check_out: e.target.value, room: room.id })}
                                        />
                                    </div>
                                </div>
                                <button type="submit" className="btn-primary" style={{ width: '100%', marginTop: '1rem' }} onClick={() => setBookingData(prev => ({ ...prev, room: room.id }))}>
                                    Book This Room
                                </button>
                            </form>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
