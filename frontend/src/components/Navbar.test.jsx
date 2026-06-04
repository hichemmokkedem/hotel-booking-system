import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect, vi } from 'vitest';
import Navbar from './Navbar';
import { AuthContext } from '../context/AuthContext';

// Mock user context
const mockUser = {
    username: 'testu',
    is_staff: false
};

const renderWithAuth = (user = null) => {
    return render(
        <AuthContext.Provider value={{ user, logout: vi.fn() }}>
            <BrowserRouter>
                <Navbar />
            </BrowserRouter>
        </AuthContext.Provider>
    );
};

describe('Navbar Component', () => {
    it('renders logo link', () => {
        renderWithAuth();
        const logo = screen.getByText('HoteLix');
        expect(logo).toBeInTheDocument();
    });

    it('shows login/register links when logged out', () => {
        renderWithAuth(null);
        expect(screen.getByText('Login')).toBeInTheDocument();
        expect(screen.getByText('Register')).toBeInTheDocument();
        expect(screen.queryByText('Logout')).not.toBeInTheDocument();
    });

    it('shows user info and logout when logged in', () => {
        renderWithAuth(mockUser);
        expect(screen.getByText('testu')).toBeInTheDocument();
        expect(screen.getByText('Logout')).toBeInTheDocument();
        expect(screen.queryByText('Login')).not.toBeInTheDocument();
    });
});
