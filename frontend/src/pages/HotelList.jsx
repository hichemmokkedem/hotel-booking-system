import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getHotels } from '../services/api';

export default function HotelList() {
    const [hotels, setHotels] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filters, setFilters] = useState({
        destination: '',
        min_price: '',
        max_price: ''
    });

    useEffect(() => {
        fetchHotels();
    }, []);

    const fetchHotels = () => {
        setLoading(true);
        getHotels(filters).then(res => {
            setHotels(res.data);
            setLoading(false);
        }).catch(err => {
            console.error(err);
            setLoading(false);
        });
    };

    const handleSearch = (e) => {
        e.preventDefault();
        fetchHotels();
    };

    if (loading) return <div className="container" style={{ textAlign: 'center', marginTop: '4rem' }}>Loading...</div>;

    return (
        <div className="container">
            <div style={{ marginBottom: '3rem', textAlign: 'center' }}>
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="url(#hotelGrad)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M9 22V12H15V22" stroke="url(#hotelGrad)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        <defs>
                            <linearGradient id="hotelGrad" x1="3" y1="2" x2="21" y2="22">
                                <stop offset="0%" stopColor="#2563eb" />
                                <stop offset="100%" stopColor="#4f46e5" />
                            </linearGradient>
                        </defs>
                    </svg>
                    <h2 style={{
                        margin: 0,
                        fontSize: '2.5rem',
                        background: 'linear-gradient(135deg, var(--primary-color), #4f46e5)',
                        WebkitBackgroundClip: 'text',
                        backgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        fontWeight: '800'
                    }}>Explore Our Hotels</h2>
                </div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', margin: 0 }}>
                    Discover exceptional stays tailored to your preferences
                </p>

                {/* Search & Filters */}
                {/* Search & Filters */}
                <form onSubmit={handleSearch} style={{
                    marginTop: '2.5rem',
                    display: 'inline-flex',
                    gap: '12px',
                    justifyContent: 'center',
                    flexWrap: 'wrap',
                    background: 'white',
                    padding: '1.5rem',
                    borderRadius: '16px',
                    boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)',
                    maxWidth: '900px',
                    width: '100%',
                    border: '1px solid rgba(0,0,0,0.05)',
                    alignItems: 'center'
                }}>
                    <div style={{ flex: '2 1 200px', position: 'relative' }}>
                        <input
                            type="text"
                            placeholder="Where to? (e.g. Paris)"
                            value={filters.destination}
                            onChange={e => setFilters({ ...filters, destination: e.target.value })}
                            style={{
                                width: '100%',
                                height: '50px',
                                padding: '0 1rem 0 2.8rem',
                                borderRadius: '8px',
                                border: '1px solid var(--border-color)',
                                fontSize: '1rem',
                                outline: 'none',
                                transition: 'border-color 0.2s',
                                background: '#f8fafc'
                            }}
                            onFocus={e => e.target.style.borderColor = 'var(--primary-color)'}
                            onBlur={e => e.target.style.borderColor = 'var(--border-color)'}
                        />
                    </div>

                    <div style={{ flex: '1 1 120px', position: 'relative' }}>
                        <input
                            type="number"
                            placeholder="Min"
                            value={filters.min_price}
                            onChange={e => setFilters({ ...filters, min_price: e.target.value })}
                            style={{
                                width: '100%',
                                height: '50px',
                                padding: '0 1rem 0 2rem',
                                borderRadius: '8px',
                                border: '1px solid var(--border-color)',
                                fontSize: '1rem',
                                background: '#f8fafc'
                            }}
                        />
                    </div>

                    <div style={{ flex: '1 1 120px', position: 'relative' }}>
                        <input
                            type="number"
                            placeholder="Max"
                            value={filters.max_price}
                            onChange={e => setFilters({ ...filters, max_price: e.target.value })}
                            style={{
                                width: '100%',
                                height: '50px',
                                padding: '0 1rem 0 2rem',
                                borderRadius: '8px',
                                border: '1px solid var(--border-color)',
                                fontSize: '1rem',
                                background: '#f8fafc'
                            }}
                        />
                    </div>

                    <button type="submit" className="btn-primary" style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.5rem',
                        height: '50px',
                        padding: '0 1.5rem',
                        fontSize: '0.95rem',
                        whiteSpace: 'nowrap',
                        flex: '0 0 auto',
                        minWidth: '120px',
                        cursor: 'pointer',
                        marginTop: '-20px'

                    }}>
                        Search
                    </button>
                </form>
            </div>
            {hotels.length === 0 ? (
                <div style={{ textAlign: 'center', marginTop: '3rem', fontSize: '1.2rem', color: 'var(--text-secondary)' }}>
                    No hotels found matching your criteria.
                </div>
            ) : (
                <div className="hotel-grid">
                    {hotels.map(hotel => (
                        <div key={hotel.id} className="hotel-card">
                            <div className="rating-badge">
                                <span>★</span> {hotel.rating}
                            </div>
                            <img src={hotel.image || 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3'} alt={hotel.name} className="hotel-img" />
                            <div className="hotel-info">
                                <h3>{hotel.name}</h3>
                                <p className="hotel-description">{hotel.description}</p>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}>
                                    <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>📍 {hotel.address}</span>
                                    <Link to={`/hotels/${hotel.id}`} className="btn-primary" style={{
                                        display: 'inline-flex',
                                        alignItems: 'center',
                                        gap: '0.5rem',
                                        padding: '0.75rem 1.5rem',
                                        fontSize: '0.95rem',
                                        whiteSpace: 'nowrap'
                                    }}>
                                        View Details
                                    </Link>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
