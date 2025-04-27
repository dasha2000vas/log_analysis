from pytest import raises

from main import get_target_report, read_line_for_handler_report


def test_handler_report_from_one_file():
    assert get_target_report(
        ["logs/app1.log"], "django.request", read_line_for_handler_report
    ) == (
        {
            "/api/v1/reviews/": {
                "debug": 0,
                "info": 5,
                "warning": 0,
                "error": 0,
                "critical": 0,
            },
            "/admin/dashboard/": {
                "debug": 0,
                "info": 6,
                "warning": 0,
                "error": 2,
                "critical": 0,
            },
            "/api/v1/users/": {
                "debug": 0,
                "info": 4,
                "warning": 0,
                "error": 0,
                "critical": 0,
            },
            "/api/v1/cart/": {
                "debug": 0,
                "info": 3,
                "warning": 0,
                "error": 0,
                "critical": 0,
            },
            "/api/v1/products/": {
                "debug": 0,
                "info": 3,
                "warning": 0,
                "error": 0,
                "critical": 0,
            },
            "/api/v1/support/": {
                "debug": 0,
                "info": 1,
                "warning": 0,
                "error": 3,
                "critical": 0,
            },
            "/api/v1/auth/login/": {
                "debug": 0,
                "info": 4,
                "warning": 0,
                "error": 1,
                "critical": 0,
            },
            "/admin/login/": {
                "debug": 0,
                "info": 5,
                "warning": 0,
                "error": 1,
                "critical": 0,
            },
            "/api/v1/checkout/": {
                "debug": 0,
                "info": 6,
                "warning": 0,
                "error": 1,
                "critical": 0,
            },
            "/api/v1/payments/": {
                "debug": 0,
                "info": 7,
                "warning": 0,
                "error": 1,
                "critical": 0,
            },
            "/api/v1/orders/": {
                "debug": 0,
                "info": 2,
                "warning": 0,
                "error": 2,
                "critical": 0,
            },
            "/api/v1/shipping/": {
                "debug": 0,
                "info": 2,
                "warning": 0,
                "error": 1,
                "critical": 0,
            },
        },
        60,
    )


def test_handler_report_from_files():
    assert get_target_report(
        ["logs/app1.log", "logs/app2.log", "logs/app3.log"],
        "django.request",
        read_line_for_handler_report,
    ) == (
        {
            "/api/v1/reviews/": {
                "debug": 0,
                "info": 20,
                "warning": 0,
                "error": 4,
                "critical": 0,
            },
            "/admin/dashboard/": {
                "debug": 0,
                "info": 13,
                "warning": 0,
                "error": 4,
                "critical": 0,
            },
            "/api/v1/users/": {
                "debug": 0,
                "info": 9,
                "warning": 0,
                "error": 3,
                "critical": 0,
            },
            "/api/v1/cart/": {
                "debug": 0,
                "info": 9,
                "warning": 0,
                "error": 1,
                "critical": 0,
            },
            "/api/v1/products/": {
                "debug": 0,
                "info": 12,
                "warning": 0,
                "error": 5,
                "critical": 0,
            },
            "/api/v1/support/": {
                "debug": 0,
                "info": 16,
                "warning": 0,
                "error": 4,
                "critical": 0,
            },
            "/api/v1/auth/login/": {
                "debug": 0,
                "info": 12,
                "warning": 0,
                "error": 2,
                "critical": 0,
            },
            "/admin/login/": {
                "debug": 0,
                "info": 12,
                "warning": 0,
                "error": 4,
                "critical": 0,
            },
            "/api/v1/checkout/": {
                "debug": 0,
                "info": 15,
                "warning": 0,
                "error": 4,
                "critical": 0,
            },
            "/api/v1/payments/": {
                "debug": 0,
                "info": 12,
                "warning": 0,
                "error": 2,
                "critical": 0,
            },
            "/api/v1/orders/": {
                "debug": 0,
                "info": 10,
                "warning": 0,
                "error": 4,
                "critical": 0,
            },
            "/api/v1/shipping/": {
                "debug": 0,
                "info": 8,
                "warning": 0,
                "error": 3,
                "critical": 0,
            },
        },
        188,
    )


def test_handler_report_file_not_found():
    with raises(
        FileNotFoundError, match="File with path logs/abracadabra.log not found"
    ):
        get_target_report(
            ["logs/abracadabra.log"], "django.request", read_line_for_handler_report
        )
