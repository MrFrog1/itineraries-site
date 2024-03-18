// In a new file, say `Modal.js`
import React from 'react';

export const Modal = ({ isOpen, children, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop">
      <div className="modal-content">
        <button onClick={onClose}>Close</button>
        {children}
      </div>
    </div>
  );
};