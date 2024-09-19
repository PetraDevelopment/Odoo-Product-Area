/** @odoo-module **/
/*
 * This file is used to restrict out of stock product from ordering and show restrict popup
 */
import VariantMixin  from 'sale.VariantMixin';

console.log(VariantMixin.getSelectedVariantValues);
var selectedVariantValues = VariantMixin.getSelectedVariantValues;


VariantMixin.getSelectedVariantValues = function($container) {
    console.log("uuuuuuuuuuuuuu348151",$container);
    var values = [];
    var unchangedValues = $container
        .find('div.oe_unchanged_value_ids')
        .data('unchanged_value_ids') || [];

    var variantsValuesSelectors = [
        'input.js_variant_change:checked',
        'select.js_variant_change'
    ];
    _.each($container.find(variantsValuesSelectors.join(', ')), function (el) {
        values.push(+$(el).val());
    });
    console.log(values[values.length - 1],'111111000')
    console.log(variantsValuesSelectors)
    return values.concat(unchangedValues);
};