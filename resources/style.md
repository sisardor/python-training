QComboBox QAbstractItemView {
    selection-background-color: #4d4d4d;
    background-color: #2c2c2c;
    border-width: 1px;
    padding: 5px 0px 5px 0px;
    border-style: solid;
    border-color: #4d4d4d;
    color: #cbcbcb;
    selection-color: #FFFFFF;
}

QComboBox {
    border-image: url(:/Images/ComboboxDefault.png) 1px 35px 1px 11px;
    border-width: 0px 34px 0px 10px;
    color: #cbcbcb;
}

QComboBox:hover {
    border-image: url(:/Images/ComboboxOver.png) 1px 35px 1px 11px;
    border-width: 0px 34px 0px 10px;
}

QComboBox:on {
    border-image: url(:/Images/ComboboxDown.png) 1px 35px 1px 11px;
    border-width: 0px 34px 0px 10px;
}

QComboBox::down-arrow {
    image: none;
    width: 16px;
    height: 16px;
}