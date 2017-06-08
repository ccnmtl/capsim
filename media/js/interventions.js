// expects window.costs, window.defaults, and window.modifiers
// to exist and be populated (dynamically in a template)

var totalBudget = 5000000;

var budgetUsed = 0;

var updateBudgetProgressBar = function() {
    var percentUsed = budgetUsed / totalBudget * 100;
    var percentRemaining = 100 - percentUsed;
    var bar = $('#budget-progress-bar .progress-bar');
    bar.attr('aria-valuenow', percentRemaining);
    bar.attr('style', 'width: ' + Math.floor(percentRemaining) + '%');
    var label = $('#budget-progress-bar .sr');
    var formatter = new Intl.NumberFormat(
        'en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
        });
    label.text(formatter.format(totalBudget - budgetUsed));
};

var overBudget = function(amount) {
    $('#run-sim-button').attr('disabled', 'disabled');
    $('#overbudget-amount').text(amount);
    $('#overbudget').show();
};

var calculateBudget = function() {
    budgetUsed = 0;
    var controls = $('.intervention-control');
    for (var i = 0; i < controls.length; i++) {
        if (controls[i].value !== '') {
            var cost = window.costs[controls[i].id][controls[i].value];
            budgetUsed += cost;
        }
    }
    applyModifiers();
    updateBudgetProgressBar();
    if (budgetUsed > totalBudget) {
        overBudget(budgetUsed - totalBudget);
    } else {
        $('#run-sim-button').removeAttr('disabled');
        $('#overbudget').hide();
    }
};

var currentValues = {};

var resetParameters = function() {
    for (var k in window.defaults) {
        if (window.defaults.hasOwnProperty(k)) {
            $('#' + k).val(window.defaults[k]);
            currentValues[k] = window.defaults[k];
        }
    }
};

var applyModifiers = function() {
    // set everything to a known state
    resetParameters();
    // then go through each control that is set and adjust accordingly
    var controls = $('.intervention-control');
    for (var i = 0; i < controls.length; i++) {
        if (controls[i].value !== '') {
            var m = window.modifiers[controls[i].id][controls[i].value];
            for (var j = 0; j < m.length; j++) {
                var paramName = m[j].param;
                var adjustment = m[j].adjustment;
                var p = $('#' + paramName);
                var newValue = currentValues[paramName] + adjustment;
                currentValues[paramName] = newValue;
                p.val(newValue);
            }
        }
    }
};

$('.intervention-control').change(calculateBudget);
$('#reset-all-button').click(function() {
    resetParameters();
    $('#intervention-form').trigger('reset');
});
