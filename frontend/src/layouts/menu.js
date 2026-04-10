import { Box, LayoutDashboard } from "lucide-react";
import { moduleConfigs } from "../config/modules";

export const menuItems = [
  { label: "Dashboard", to: "/dashboard", icon: LayoutDashboard },
  ...moduleConfigs.map((item) => ({
    label: item.label,
    to: `/modules/${item.route}`,
    icon: Box,
    permission: item.permission,
  })),
];
