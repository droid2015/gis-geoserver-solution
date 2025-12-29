import React, { useState } from 'react';
import './Sidebar.css';

const Sidebar = ({ children }) => {
  const [activeTab, setActiveTab] = useState('layers');

  const tabs = [
    { id: 'layers', label: 'Layers' },
    { id: 'upload', label: 'Upload' },
    { id: 'query', label: 'Query' },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div className="sidebar-content">
        {React.Children.map(children, (child) => {
          if (child && child.props.tabId === activeTab) {
            return child;
          }
          return null;
        })}
      </div>
    </div>
  );
};

export const SidebarTab = ({ tabId, children }) => {
  return <div className="sidebar-tab-content">{children}</div>;
};

export default Sidebar;
