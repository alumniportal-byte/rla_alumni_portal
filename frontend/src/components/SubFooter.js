import Link from 'next/link'
import React from 'react'

const SubFooter = () => {
const linkStyle = {
  color: 'gold',
  textDecoration: 'none',
  fontWeight: '500', 
};
const spanStyle = {
    color: 'white'
}
  return (
    <div className="subfooter">
        <span style={spanStyle}>Copyright &copy; 2026 - All Rights Reserved</span>
        <span style={spanStyle}>Designed & Developed by <Link href="https://www.linkedin.com/in/anurag-gusain04" style={linkStyle} target="_blank" rel="noopener noreferrer">Anurag Gusain</Link> & <Link href="https://www.linkedin.com/in/kanishk-chauhan-1436253b1/" style={linkStyle} target="_blank" rel="noopener noreferrer">Kanishk Chauhan</Link></span>
    </div>
  )
}

export default SubFooter