import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

// Mock WebSocket
global.WebSocket = vi.fn().mockImplementation(() => ({
    send: vi.fn(),
    close: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
}));

// Mock SimulationCanvas
vi.mock('./components/SimulationCanvas', () => ({
    default: () => <div data-testid="simulation-canvas">Mock Canvas</div>
}));

describe('App', () => {
    it('renders without crashing', () => {
        render(<App />);
        // Check if ControlPanel is rendered
        expect(screen.getByText(/Control Panel/i)).toBeInTheDocument();
    });
});
