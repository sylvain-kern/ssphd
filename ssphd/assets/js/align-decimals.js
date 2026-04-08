/**
 * Align numeric table columns on the decimal point
 * This script splits numeric values into integer and decimal parts
 * and aligns them using CSS for proper visual alignment
 */

class DecimalAligner {
  constructor(options = {}) {
    this.decimalSeparator = options.decimalSeparator || '.';
    this.className = options.className || 'decimal-aligned';
    this.integerClass = options.integerClass || 'integer-part';
    this.decimalClass = options.decimalClass || 'decimal-part';
  }

  /**
   * Check if a string is a numeric value
   */
  isNumeric(value) {
    const cleanValue = value.trim().replace(/[,\s]/g, '');
    return !isNaN(cleanValue) && !isNaN(parseFloat(cleanValue));
  }

  /**
   * Split a numeric value into integer and decimal parts
   */
  splitNumber(value) {
    const cleanValue = value.trim();
    const parts = cleanValue.split(this.decimalSeparator);
    
    return {
      integer: parts[0] || '0',
      decimal: parts[1] ? this.decimalSeparator + parts[1] : ''
    };
  }

  /**
   * Create aligned HTML structure for a number
   */
  createAlignedCell(number) {
    const parts = this.splitNumber(number);
    const span = document.createElement('span');
    span.className = this.className;
    
    const integerSpan = document.createElement('span');
    integerSpan.className = this.integerClass;
    integerSpan.textContent = parts.integer;
    
    const decimalSpan = document.createElement('span');
    decimalSpan.className = this.decimalClass;
    decimalSpan.textContent = parts.decimal;
    
    span.appendChild(integerSpan);
    span.appendChild(decimalSpan);
    
    return span;
  }

  /**
   * Align a specific table column
   */
  alignColumn(table, columnIndex) {
    const rows = table.querySelectorAll('tr');
    const cells = [];
    
    // Collect all cells in the column
    rows.forEach(row => {
      const cell = row.children[columnIndex];
      if (cell) {
        cells.push(cell);
      }
    });
    
    // Check if column contains numeric data
    const isNumericColumn = cells.some(cell => {
      const text = cell.textContent.trim();
      return text && this.isNumeric(text);
    });
    
    if (!isNumericColumn) {
      return false;
    }
    
    // Align numeric cells
    cells.forEach(cell => {
      const text = cell.textContent.trim();
      if (text && this.isNumeric(text)) {
        cell.textContent = '';
        cell.appendChild(this.createAlignedCell(text));
      }
    });
    
    return true;
  }

  /**
   * Automatically align all numeric columns in a table
   */
  alignTable(table) {
    if (!table || !table.rows || table.rows.length === 0) {
      return;
    }
    
    const numColumns = table.rows[0].children.length;
    
    for (let i = 0; i < numColumns; i++) {
      this.alignColumn(table, i);
    }
  }

  /**
   * Align all tables with a specific selector
   */
  alignAll(selector = 'table') {
    const tables = document.querySelectorAll(selector);
    tables.forEach(table => this.alignTable(table));
  }

  /**
   * Inject required CSS styles
   */
  injectStyles() {
    const styleId = 'decimal-aligner-styles';
    
    // Don't inject twice
    if (document.getElementById(styleId)) {
      return;
    }
    
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      .${this.className} {
        display: inline-flex;
        width: 100%;
        justify-content: flex-end;
      }
      
      .${this.integerClass} {
        text-align: right;
      }
      
      .${this.decimalClass} {
        text-align: left;
        min-width: 0;
      }
      
      td .${this.className},
      th .${this.className} {
        font-variant-numeric: tabular-nums;
      }
    `;
    
    document.head.appendChild(style);
  }
}

// Usage examples and initialization
if (typeof module !== 'undefined' && module.exports) {
  module.exports = DecimalAligner;
} else if (typeof window !== 'undefined') {
  window.DecimalAligner = DecimalAligner;
  
  // Auto-initialize on page load
  document.addEventListener('DOMContentLoaded', () => {
    const aligner = new DecimalAligner();
    aligner.injectStyles();
    
    // Align tables with data-align-decimals attribute
    aligner.alignAll('table[data-align-decimals]');
  });
}
