import React from 'react';
import Header from './Header';
import './Layout.css';

const Layout = ({ children }) => {
  return (
    <div className="app-layout">
      <Header />
      <main className="app-main">{children}</main>
    </div>
  );
};

export default Layout;
